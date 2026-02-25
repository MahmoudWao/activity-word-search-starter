import csv
from datetime import datetime, timedelta
from pathlib import Path
from config import (
    DAILY_ENTRIES_CSV, WEEKLY_SUMMARIES_CSV, ATTRIBUTES,
    RUNNING_AVERAGE_WINDOW
)


class DailyEntry:
    def __init__(self, date, week_type, mental_resilience, physical_energy,
                 emotional_balance, stress_level, productivity,
                 running_avg_mental=None, running_avg_physical=None,
                 running_avg_emotional=None, running_avg_stress=None,
                 running_avg_productivity=None):
        self.date = date  # YYYY-MM-DD
        self.week_type = week_type  # "36h" or "48h"
        self.mental_resilience = int(mental_resilience)
        self.physical_energy = int(physical_energy)
        self.emotional_balance = int(emotional_balance)
        self.stress_level = int(stress_level)  # 10=calm, 1=chaos
        self.productivity = int(productivity)
        self.running_avg_mental = running_avg_mental
        self.running_avg_physical = running_avg_physical
        self.running_avg_emotional = running_avg_emotional
        self.running_avg_stress = running_avg_stress
        self.running_avg_productivity = running_avg_productivity

    def validate(self):
        """Validate entry data"""
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if self.week_type not in ["36h", "48h"]:
            raise ValueError("Week type must be 36h or 48h")

        for attr in ATTRIBUTES:
            val = getattr(self, attr)
            if not (1 <= val <= 10):
                raise ValueError(f"{attr} must be between 1 and 10")

    def to_dict(self):
        return {
            "date": self.date,
            "week_type": self.week_type,
            "mental_resilience": self.mental_resilience,
            "physical_energy": self.physical_energy,
            "emotional_balance": self.emotional_balance,
            "stress_level": self.stress_level,
            "productivity": self.productivity,
            "running_avg_mental": self.running_avg_mental,
            "running_avg_physical": self.running_avg_physical,
            "running_avg_emotional": self.running_avg_emotional,
            "running_avg_stress": self.running_avg_stress,
            "running_avg_productivity": self.running_avg_productivity,
        }

    @staticmethod
    def from_dict(data):
        return DailyEntry(**data)


class WeeklySummary:
    def __init__(self, week_ending, week_type, mental_resilience_avg,
                 physical_energy_avg, emotional_balance_avg, stress_level_avg,
                 productivity_avg):
        self.week_ending = week_ending  # YYYY-MM-DD (Sunday)
        self.week_type = week_type
        self.mental_resilience_avg = float(mental_resilience_avg)
        self.physical_energy_avg = float(physical_energy_avg)
        self.emotional_balance_avg = float(emotional_balance_avg)
        self.stress_level_avg = float(stress_level_avg)
        self.productivity_avg = float(productivity_avg)

    def validate(self):
        """Validate weekly summary"""
        try:
            date = datetime.strptime(self.week_ending, "%Y-%m-%d")
            # Check if it's a Sunday (weekday 6)
            if date.weekday() != 6:
                raise ValueError("week_ending must be a Sunday")
        except ValueError as e:
            raise ValueError(f"Invalid week_ending: {e}")

        if self.week_type not in ["36h", "48h"]:
            raise ValueError("Week type must be 36h or 48h")

        for attr in ["mental_resilience_avg", "physical_energy_avg",
                     "emotional_balance_avg", "stress_level_avg", "productivity_avg"]:
            val = getattr(self, attr)
            if not (1 <= val <= 10):
                raise ValueError(f"{attr} must be between 1 and 10")

    def to_dict(self):
        return {
            "week_ending": self.week_ending,
            "week_type": self.week_type,
            "mental_resilience_avg": self.mental_resilience_avg,
            "physical_energy_avg": self.physical_energy_avg,
            "emotional_balance_avg": self.emotional_balance_avg,
            "stress_level_avg": self.stress_level_avg,
            "productivity_avg": self.productivity_avg,
        }

    @staticmethod
    def from_dict(data):
        return WeeklySummary(**data)


class CSVManager:
    @staticmethod
    def read_daily_entries():
        """Read all daily entries from CSV"""
        if not DAILY_ENTRIES_CSV.exists():
            return []

        entries = []
        try:
            with open(DAILY_ENTRIES_CSV, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entries.append(DailyEntry.from_dict(row))
        except Exception as e:
            print(f"Error reading daily entries: {e}")
            return []

        return entries

    @staticmethod
    def write_daily_entries(entries):
        """Write daily entries to CSV"""
        DAILY_ENTRIES_CSV.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "date", "week_type", "mental_resilience", "physical_energy",
            "emotional_balance", "stress_level", "productivity",
            "running_avg_mental", "running_avg_physical", "running_avg_emotional",
            "running_avg_stress", "running_avg_productivity"
        ]

        try:
            with open(DAILY_ENTRIES_CSV, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entry in entries:
                    writer.writerow(entry.to_dict())
        except Exception as e:
            print(f"Error writing daily entries: {e}")
            raise

    @staticmethod
    def read_weekly_summaries():
        """Read all weekly summaries from CSV"""
        if not WEEKLY_SUMMARIES_CSV.exists():
            return []

        summaries = []
        try:
            with open(WEEKLY_SUMMARIES_CSV, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    summaries.append(WeeklySummary.from_dict(row))
        except Exception as e:
            print(f"Error reading weekly summaries: {e}")
            return []

        return summaries

    @staticmethod
    def write_weekly_summaries(summaries):
        """Write weekly summaries to CSV"""
        WEEKLY_SUMMARIES_CSV.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "week_ending", "week_type", "mental_resilience_avg",
            "physical_energy_avg", "emotional_balance_avg", "stress_level_avg",
            "productivity_avg"
        ]

        try:
            with open(WEEKLY_SUMMARIES_CSV, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for summary in summaries:
                    writer.writerow(summary.to_dict())
        except Exception as e:
            print(f"Error writing weekly summaries: {e}")
            raise
