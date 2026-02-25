#!/usr/bin/env python3
"""
Daily Pentagon Tracker — Automatic Runner

Can be invoked by cron or a scheduler to:
  • Send a desktop notification reminding you to log your entry
  • Open the tracker in a terminal for interactive logging
  • Regenerate all charts from existing data

Usage:
  python3 daily_update.py notify     # Send a reminder notification
  python3 daily_update.py refresh    # Regenerate all charts from saved data
  python3 daily_update.py log        # Open the interactive tracker to log today
  python3 daily_update.py setup      # Print cron setup instructions
"""

import subprocess
import sys
from pathlib import Path

TRACKER = Path(__file__).parent / "pentagon_tracker.py"


def send_notification() -> None:
    """Send a desktop notification reminding the user to log their day."""
    title = "Pentagon Tracker"
    message = "Time to log your daily pentagon entry!"

    system = sys.platform
    try:
        if system == "linux":
            subprocess.run(["notify-send", title, message], check=True)
        elif system == "darwin":
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=True)
        else:
            print(f"  [{title}] {message}")
    except FileNotFoundError:
        print(f"  [{title}] {message}")
        print("  (Install notify-send for desktop notifications on Linux)")


def refresh_charts() -> None:
    """Regenerate all charts from the existing tracker data."""
    # Import tracker module directly
    sys.path.insert(0, str(Path(__file__).parent))
    import pentagon_tracker as pt

    data = pt.load_data()
    if not data:
        print("  No data found. Nothing to refresh.")
        return

    pt.regenerate_all_charts(data)
    print(f"  Refreshed charts for {len(data)} entries.")


def open_tracker() -> None:
    """Launch the interactive tracker."""
    subprocess.run([sys.executable, str(TRACKER)])


def print_setup_instructions() -> None:
    """Print cron setup instructions for the user's platform."""
    script_path = Path(__file__).resolve()
    python_path = sys.executable

    print("""
╔══════════════════════════════════════════════════════╗
║       AUTOMATIC UPDATE SETUP INSTRUCTIONS            ║
╚══════════════════════════════════════════════════════╝

── Linux / macOS (cron) ──────────────────────────────

  1. Open your crontab:
     crontab -e

  2. Add one or more of these lines:

     # Daily reminder notification at 5:00 PM
     0 17 * * * {python} {script} notify

     # Refresh all charts every night at midnight
     0 0 * * * {python} {script} refresh

── macOS (launchd — preferred) ───────────────────────

  Create ~/Library/LaunchAgents/com.pentagon-tracker.daily.plist
  with a WatchPaths entry pointing to tracker_data.json for
  automatic chart regeneration on every data change.

── Windows (Task Scheduler) ──────────────────────────

  1. Open Task Scheduler
  2. Create a new task with trigger "Daily" at your preferred time
  3. Action: Start a program
     Program: {python}
     Arguments: {script} notify

── Test it now ───────────────────────────────────────

  {python} {script} notify     # test notification
  {python} {script} refresh    # regenerate charts
""".format(python=python_path, script=script_path))


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 daily_update.py [notify|refresh|log|setup]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "notify":
        send_notification()
    elif command == "refresh":
        refresh_charts()
    elif command == "log":
        open_tracker()
    elif command == "setup":
        print_setup_instructions()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python3 daily_update.py [notify|refresh|log|setup]")
        sys.exit(1)


if __name__ == "__main__":
    main()
