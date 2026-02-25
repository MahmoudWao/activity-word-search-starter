import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data directory
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# CSV file paths
DAILY_ENTRIES_CSV = DATA_DIR / "daily_entries.csv"
WEEKLY_SUMMARIES_CSV = DATA_DIR / "weekly_summaries.csv"

# Constants
ATTRIBUTES = [
    "mental_resilience",
    "physical_energy",
    "emotional_balance",
    "stress_level",
    "productivity"
]

ATTRIBUTE_LABELS = {
    "mental_resilience": "Mental Resilience",
    "physical_energy": "Physical Energy",
    "emotional_balance": "Emotional Balance",
    "stress_level": "Low Stress",
    "productivity": "Productivity"
}

DAILY_LOG_ROWS = 60  # About 2 months
RUNNING_AVERAGE_WINDOW = 14  # Days

# Theme colors
HEATMAP_COLORS = {
    "red": "#FF4444",
    "amber": "#FFB444",
    "green": "#44FF44"
}

DARK_THEME = {
    "bg_primary": "#1a1a1a",
    "bg_secondary": "#2a2a2a",
    "text_primary": "#e0e0e0",
    "accent": "#00d4ff"
}
