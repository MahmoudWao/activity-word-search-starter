from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
from app.models import DailyEntry, CSVManager
from app.calculations import (
    get_heatmap_color, calculate_running_averages, get_sorted_entries,
    get_week_ending_date, generate_weekly_summary
)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Serve the main page"""
    return render_template('base.html')


@main_bp.route('/api/daily-log', methods=['GET'])
def get_daily_log():
    """Retrieve all daily entries"""
    try:
        entries = CSVManager.read_daily_entries()
        entries = get_sorted_entries(entries)
        data = [entry.to_dict() for entry in entries]
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main_bp.route('/api/daily-log', methods=['POST'])
def save_daily_entry():
    """Save a new daily entry"""
    try:
        data = request.json

        # Create and validate entry
        entry = DailyEntry(
            date=data.get('date'),
            week_type=data.get('week_type'),
            mental_resilience=data.get('mental_resilience'),
            physical_energy=data.get('physical_energy'),
            emotional_balance=data.get('emotional_balance'),
            stress_level=data.get('stress_level'),
            productivity=data.get('productivity')
        )
        entry.validate()

        # Read existing entries
        entries = CSVManager.read_daily_entries()
        entries = get_sorted_entries(entries)

        # Check if entry for this date already exists
        existing_idx = next(
            (i for i, e in enumerate(entries) if e.date == entry.date),
            None
        )

        if existing_idx is not None:
            entries[existing_idx] = entry
        else:
            entries.append(entry)

        # Recalculate running averages
        entries = get_sorted_entries(entries)
        calculate_running_averages(entries)

        # Save to CSV
        CSVManager.write_daily_entries(entries)

        # Check if this is a Sunday entry and generate weekly summary
        entry_date = datetime.strptime(entry.date, "%Y-%m-%d").date()
        if entry_date.weekday() == 6:  # Sunday
            weekly_summary = generate_weekly_summary(entries, entry_date)
            if weekly_summary:
                summaries = CSVManager.read_weekly_summaries()
                # Check if summary for this week already exists
                existing_summary_idx = next(
                    (i for i, s in enumerate(summaries) if s.week_ending == weekly_summary.week_ending),
                    None
                )
                if existing_summary_idx is not None:
                    summaries[existing_summary_idx] = weekly_summary
                else:
                    summaries.append(weekly_summary)
                CSVManager.write_weekly_summaries(summaries)

        return jsonify({
            "success": True,
            "message": "Entry saved successfully",
            "data": entry.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main_bp.route('/api/weekly-summary', methods=['GET'])
def get_weekly_summaries():
    """Retrieve all weekly summaries"""
    try:
        summaries = CSVManager.read_weekly_summaries()
        # Sort by week_ending descending (newest first)
        summaries = sorted(
            summaries,
            key=lambda s: s.week_ending,
            reverse=True
        )
        data = [summary.to_dict() for summary in summaries]
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main_bp.route('/api/weekly-summary', methods=['POST'])
def save_weekly_summary():
    """Save or update a weekly summary"""
    try:
        data = request.json

        # Create and validate summary
        summary = WeeklySummary(
            week_ending=data.get('week_ending'),
            week_type=data.get('week_type'),
            mental_resilience_avg=data.get('mental_resilience_avg'),
            physical_energy_avg=data.get('physical_energy_avg'),
            emotional_balance_avg=data.get('emotional_balance_avg'),
            stress_level_avg=data.get('stress_level_avg'),
            productivity_avg=data.get('productivity_avg')
        )
        summary.validate()

        # Read existing summaries
        summaries = CSVManager.read_weekly_summaries()

        # Check if summary for this week already exists
        existing_idx = next(
            (i for i, s in enumerate(summaries) if s.week_ending == summary.week_ending),
            None
        )

        if existing_idx is not None:
            summaries[existing_idx] = summary
        else:
            summaries.append(summary)

        # Save to CSV
        CSVManager.write_weekly_summaries(summaries)

        return jsonify({
            "success": True,
            "message": "Weekly summary saved successfully",
            "data": summary.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main_bp.route('/api/weekly-averages/<date>', methods=['GET'])
def get_weekly_averages(date):
    """Calculate weekly averages for a given date"""
    try:
        entries = CSVManager.read_daily_entries()
        entries = get_sorted_entries(entries)

        # Generate summary for the week ending on or after the given date
        week_end = get_week_ending_date(date)
        summary = generate_weekly_summary(entries, week_end)

        if summary:
            return jsonify({
                "success": True,
                "data": summary.to_dict()
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "No entries for this week"
            }), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Import after defining routes to avoid circular imports
from app.models import WeeklySummary
