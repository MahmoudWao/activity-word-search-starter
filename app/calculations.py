from datetime import datetime, timedelta
from config import HEATMAP_COLORS, RUNNING_AVERAGE_WINDOW
from app.models import WeeklySummary


def get_heatmap_color(score, attribute=""):
    """
    Get heatmap color based on score (1-10).
    Red (1-3) -> Amber (4-6) -> Green (7-10)

    For stress_level, the score is already stored inverted (10=calm, 1=chaos),
    so we use it directly.
    """
    if not (1 <= score <= 10):
        return "#CCCCCC"  # Gray for invalid

    if score <= 3:
        return HEATMAP_COLORS["red"]
    elif score <= 6:
        return HEATMAP_COLORS["amber"]
    else:
        return HEATMAP_COLORS["green"]


def calculate_running_averages(entries, window=RUNNING_AVERAGE_WINDOW):
    """
    Calculate running averages for all entries.
    Updates entries in place with running average values.
    """
    attributes = [
        "mental_resilience",
        "physical_energy",
        "emotional_balance",
        "stress_level",
        "productivity"
    ]

    for i, entry in enumerate(entries):
        start_idx = max(0, i - window + 1)
        window_entries = entries[start_idx:i + 1]

        for attr in attributes:
            avg_key = f"running_avg_{attr.split('_')[0]}"
            if attr == "mental_resilience":
                avg_key = "running_avg_mental"
            elif attr == "physical_energy":
                avg_key = "running_avg_physical"
            elif attr == "emotional_balance":
                avg_key = "running_avg_emotional"
            elif attr == "stress_level":
                avg_key = "running_avg_stress"
            elif attr == "productivity":
                avg_key = "running_avg_productivity"

            values = [getattr(e, attr) for e in window_entries]
            avg = sum(values) / len(values) if values else 0.0
            setattr(entry, avg_key, round(avg, 2))


def get_week_range(date_obj):
    """
    Get the Monday-Sunday range for a given date.
    Returns (monday_date, sunday_date) as date objects.
    """
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()

    weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
    monday = date_obj - timedelta(days=weekday)
    sunday = monday + timedelta(days=6)
    return (monday, sunday)


def get_week_ending_date(date_obj):
    """Get the Sunday (week ending date) for a given date."""
    _, sunday = get_week_range(date_obj)
    return sunday


def generate_weekly_summary(entries, week_end_date):
    """
    Generate a weekly summary for entries in the week ending on week_end_date.
    week_end_date should be a Sunday.
    """
    if isinstance(week_end_date, str):
        week_end_date = datetime.strptime(week_end_date, "%Y-%m-%d").date()

    week_start, week_end = get_week_range(week_end_date)

    # Filter entries for this week
    week_entries = [
        e for e in entries
        if isinstance(e.date, str)
        and week_start <= datetime.strptime(e.date, "%Y-%m-%d").date() <= week_end
    ]

    if not week_entries:
        return None

    # Calculate averages
    mental_avg = sum(e.mental_resilience for e in week_entries) / len(week_entries)
    physical_avg = sum(e.physical_energy for e in week_entries) / len(week_entries)
    emotional_avg = sum(e.emotional_balance for e in week_entries) / len(week_entries)
    stress_avg = sum(e.stress_level for e in week_entries) / len(week_entries)
    productivity_avg = sum(e.productivity for e in week_entries) / len(week_entries)

    # Determine week type (36h or 48h)
    week_type_counts = {}
    for e in week_entries:
        week_type_counts[e.week_type] = week_type_counts.get(e.week_type, 0) + 1
    week_type = max(week_type_counts, key=week_type_counts.get) if week_type_counts else "36h"

    summary = WeeklySummary(
        week_ending=week_end.strftime("%Y-%m-%d"),
        week_type=week_type,
        mental_resilience_avg=round(mental_avg, 2),
        physical_energy_avg=round(physical_avg, 2),
        emotional_balance_avg=round(emotional_avg, 2),
        stress_level_avg=round(stress_avg, 2),
        productivity_avg=round(productivity_avg, 2),
    )

    return summary


def get_sorted_entries(entries):
    """Sort entries by date"""
    try:
        return sorted(entries, key=lambda e: datetime.strptime(e.date, "%Y-%m-%d"))
    except:
        return entries
