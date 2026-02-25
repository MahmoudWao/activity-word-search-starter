#!/usr/bin/env python3
"""
Daily Pentagon Chart Tracker

Tracks five daily work attributes on a radar (pentagon) chart:
  1. Sleep — how rested you actually felt
  2. Energy/Physical Readiness — body condition on the floor
  3. Focus/Mental Clarity — sharpness and cognitive performance
  4. Stress/Pressure Level — inverse scale (5 = low stress, 1 = high stress)
  5. Motivation/Morale — engagement and drive

Each attribute is rated 1–5. Entries are stored in a local JSON file
and can be visualized as a filled pentagon chart.
"""

import json
import os
import sys
from datetime import date, datetime
from math import pi
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend; saves to file
import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).parent / "tracker_data.json"

CATEGORIES = [
    "Sleep",
    "Energy / Physical Readiness",
    "Focus / Mental Clarity",
    "Stress / Pressure (5=low)",
    "Motivation / Morale",
]

CATEGORY_DESCRIPTIONS = {
    "Sleep": "How rested you actually felt (not just hours logged)",
    "Energy / Physical Readiness": "How your body felt — soreness, fatigue, nutrition",
    "Focus / Mental Clarity": "How sharp were you — troubleshooting, reading tickets, safety",
    "Stress / Pressure (5=low)": "Inverse: 5 = calm day, 1 = fires everywhere",
    "Motivation / Morale": "How engaged you felt with the work",
}


# ---------------------------------------------------------------------------
# Data persistence
# ---------------------------------------------------------------------------

def load_data() -> dict:
    """Load existing tracker data from JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data: dict) -> None:
    """Save tracker data to JSON file and regenerate all charts."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    regenerate_all_charts(data)


def regenerate_all_charts(data: dict) -> None:
    """Regenerate pentagon chart PNGs for every entry in the dataset."""
    for entry_date, entry in data.items():
        build_pentagon_chart(entry_date, entry["scores"])
    if len(data) >= 2:
        build_comparison_chart(data, sorted(data.keys()))


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def get_rating(category: str) -> int:
    """Prompt user for a 1–5 rating for a given category."""
    desc = CATEGORY_DESCRIPTIONS[category]
    while True:
        try:
            val = int(input(f"  {category}\n    ({desc})\n    Rate 1–5: "))
            if 1 <= val <= 5:
                return val
            print("    Please enter a number between 1 and 5.")
        except ValueError:
            print("    Invalid input. Enter a number 1–5.")


def get_date_input() -> str:
    """Ask user for a date or default to today."""
    today = date.today().isoformat()
    raw = input(f"\nDate (YYYY-MM-DD) [default: {today}]: ").strip()
    if not raw:
        return today
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        print(f"  Invalid format. Using today's date: {today}")
        return today


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------

def build_pentagon_chart(entry_date: str, scores: list[int], out_path: str | None = None) -> str:
    """Generate a filled pentagon radar chart and save it as a PNG.

    Returns the path to the saved image.
    """
    num_vars = len(CATEGORIES)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # close the polygon

    values = scores + scores[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Draw the outer boundary ring at 5
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8, color="grey")

    # Category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(CATEGORIES, fontsize=9, fontweight="bold")

    # Plot data
    ax.plot(angles, values, linewidth=2, linestyle="solid", color="#4A90D9")
    ax.fill(angles, values, alpha=0.25, color="#4A90D9")

    # Dot markers
    ax.scatter(angles[:-1], scores, s=60, color="#4A90D9", zorder=5)

    # Score labels next to each point
    for angle, score in zip(angles[:-1], scores):
        ax.annotate(
            str(score),
            xy=(angle, score),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=11,
            fontweight="bold",
            color="#2C3E50",
        )

    avg = sum(scores) / len(scores)
    ax.set_title(
        f"Daily Pentagon — {entry_date}\nOverall avg: {avg:.1f} / 5",
        fontsize=13,
        fontweight="bold",
        pad=24,
    )

    if out_path is None:
        out_path = str(Path(__file__).parent / f"pentagon_{entry_date}.png")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def build_comparison_chart(data: dict, dates: list[str], out_path: str | None = None) -> str:
    """Overlay multiple days on one pentagon chart for comparison."""
    num_vars = len(CATEGORIES)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    colors = ["#4A90D9", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8, color="grey")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(CATEGORIES, fontsize=9, fontweight="bold")

    for i, d in enumerate(dates):
        scores = data[d]["scores"]
        values = scores + scores[:1]
        color = colors[i % len(colors)]
        ax.plot(angles, values, linewidth=2, label=d, color=color)
        ax.fill(angles, values, alpha=0.08, color=color)

    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=9)
    ax.set_title("Pentagon Comparison", fontsize=13, fontweight="bold", pad=24)

    if out_path is None:
        out_path = str(Path(__file__).parent / "pentagon_comparison.png")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------

def log_entry() -> None:
    """Record a new daily entry."""
    data = load_data()
    entry_date = get_date_input()

    if entry_date in data:
        overwrite = input(f"  Entry for {entry_date} already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != "y":
            print("  Cancelled.")
            return

    print(f"\nRate each attribute 1–5 for {entry_date}:\n")
    scores = [get_rating(cat) for cat in CATEGORIES]

    data[entry_date] = {
        "scores": scores,
        "logged_at": datetime.now().isoformat(),
    }
    save_data(data)

    path = build_pentagon_chart(entry_date, scores)
    print(f"\n  Entry saved! Chart → {path}")


def view_entry() -> None:
    """View / regenerate chart for a specific date."""
    data = load_data()
    if not data:
        print("  No entries yet.")
        return

    print("\nAvailable dates:")
    for d in sorted(data.keys()):
        scores = data[d]["scores"]
        avg = sum(scores) / len(scores)
        print(f"  {d}  (avg {avg:.1f})")

    entry_date = input("\nEnter date to view (YYYY-MM-DD): ").strip()
    if entry_date not in data:
        print("  No entry found for that date.")
        return

    scores = data[entry_date]["scores"]
    print(f"\n  Scores for {entry_date}:")
    for cat, s in zip(CATEGORIES, scores):
        print(f"    {cat}: {s}")
    avg = sum(scores) / len(scores)
    print(f"    ── Overall avg: {avg:.1f}")

    path = build_pentagon_chart(entry_date, scores)
    print(f"  Chart → {path}")


def compare_entries() -> None:
    """Overlay multiple days for side-by-side comparison."""
    data = load_data()
    if len(data) < 2:
        print("  Need at least 2 entries to compare.")
        return

    sorted_dates = sorted(data.keys())
    print("\nAvailable dates:")
    for i, d in enumerate(sorted_dates, 1):
        print(f"  {i}. {d}")

    raw = input("\nEnter date numbers to compare (comma-separated, e.g. 1,3,5): ").strip()
    try:
        indices = [int(x.strip()) - 1 for x in raw.split(",")]
        chosen = [sorted_dates[i] for i in indices]
    except (ValueError, IndexError):
        print("  Invalid selection.")
        return

    path = build_comparison_chart(data, chosen)
    print(f"  Comparison chart → {path}")


def show_trends() -> None:
    """Show a simple text-based trend of averages over logged dates."""
    data = load_data()
    if not data:
        print("  No entries yet.")
        return

    sorted_dates = sorted(data.keys())
    print("\n  Date         Avg   Sleep  Energy  Focus  Stress  Morale")
    print("  " + "─" * 60)
    for d in sorted_dates:
        s = data[d]["scores"]
        avg = sum(s) / len(s)
        print(f"  {d}  {avg:.1f}   {s[0]}      {s[1]}       {s[2]}      {s[3]}       {s[4]}")
    print()


def delete_entry() -> None:
    """Delete an entry by date."""
    data = load_data()
    if not data:
        print("  No entries to delete.")
        return

    print("\nAvailable dates:")
    for d in sorted(data.keys()):
        print(f"  {d}")

    entry_date = input("\nDate to delete (YYYY-MM-DD): ").strip()
    if entry_date not in data:
        print("  No entry found.")
        return

    confirm = input(f"  Delete {entry_date}? (y/n): ").strip().lower()
    if confirm == "y":
        del data[entry_date]
        save_data(data)
        print("  Deleted.")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

MENU = """
╔══════════════════════════════════════╗
║   DAILY PENTAGON CHART TRACKER      ║
╠══════════════════════════════════════╣
║  1. Log today's entry               ║
║  2. View / regenerate a chart       ║
║  3. Compare multiple days           ║
║  4. Show trends table               ║
║  5. Delete an entry                 ║
║  6. Quit                            ║
╚══════════════════════════════════════╝"""


def main() -> None:
    print(MENU)
    while True:
        choice = input("\nChoose (1-6): ").strip()
        if choice == "1":
            log_entry()
        elif choice == "2":
            view_entry()
        elif choice == "3":
            compare_entries()
        elif choice == "4":
            show_trends()
        elif choice == "5":
            delete_entry()
        elif choice == "6":
            print("  Stay sharp out there. ✌️")
            break
        else:
            print("  Enter 1–6.")
        print(MENU)


if __name__ == "__main__":
    main()
