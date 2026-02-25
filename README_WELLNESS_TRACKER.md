# Wellness Tracker

A web-based wellness tracking application that helps you monitor your well-being across 5 key dimensions: Mental Resilience, Physical Energy, Emotional Balance, Low Stress, and Productivity.

## Features

### 📊 Daily Log Tab
- Track 60 days (~2 months) of wellness data
- Score 5 attributes on a 1-10 scale
- **Heat-map color coding**: Red (1-3) → Amber (4-6) → Green (7-10)
- Automatic running averages (14-day rolling average)
- Enter date, week type (36h or 48h), and all 5 scores

### 📈 Weekly Summary Tab
- Automatic weekly average calculation
- **Pentagon radar chart** visualization of your wellness shape
- Bigger pentagon = better week
- View historical weekly trends
- Spot wellness imbalances (e.g., high focus but low motivation)

### 📚 Instructions Tab
- Scoring rubric for each dimension
- Detailed descriptions for each score level
- Usage guide
- Special note on Low Stress inversion (10 = calm, 1 = chaos)

### 🌙 Dark Theme
- Easy on the eyes
- Modern, clean interface
- Consistent color scheme throughout

## Installation

### Requirements
- Python 3.7+
- Flask 2.3.0
- python-dateutil 2.8.2

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser to `http://localhost:5000`

## Data Storage

Data is stored in CSV files in the `data/` directory:

- **daily_entries.csv**: All daily wellness entries with running averages
- **weekly_summaries.csv**: Weekly summaries with radar chart data

## Scoring Guide

### Mental Resilience (1-10)
- **1-3**: Overwhelmed, unfocused, struggling with decisions
- **4-6**: Managing okay, some mental fatigue
- **7-10**: Sharp, clear-headed, handling challenges well

### Physical Energy (1-10)
- **1-3**: Exhausted, low stamina, sluggish
- **4-6**: Average energy, getting by
- **7-10**: Energetic, well-rested, good stamina

### Emotional Balance (1-10)
- **1-3**: Irritable, anxious, emotionally volatile
- **4-6**: Stable but some mood fluctuations
- **7-10**: Calm, content, emotionally regulated

### Low Stress (1-10) ⚠️ INVERTED
- **1**: Chaotic, high pressure, reactive
- **4-6**: Moderate stress, manageable
- **10**: Calm, in control, proactive

*Note: Low Stress is inverted to ensure all scores read the same direction on the radar chart.*

### Productivity (1-10)
- **1-3**: Procrastinating, blocked, unproductive
- **4-6**: Making progress, some friction
- **7-10**: Focused, efficient, shipping

## How It Works

1. **Daily Entry**: Each day (or shift), enter your date, week type, and rate yourself on 5 dimensions
2. **Heat-Map Colors**: Cells automatically color-code based on your scores for quick visual assessment
3. **Running Averages**: Automatically calculated for the last 14 days
4. **Sunday Trigger**: On Sundays, the system auto-generates your weekly averages
5. **Radar Chart**: Your weekly pentagon chart shows your "wellness shape" for easy pattern spotting

## Project Structure

```
wellness-tracker/
├── app.py                 # Main entry point
├── config.py              # Configuration and constants
├── requirements.txt       # Python dependencies
├── README_WELLNESS_TRACKER.md  # This file
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── routes.py          # Flask routes and API endpoints
│   ├── models.py          # Data models and CSV handling
│   └── calculations.py    # Business logic (averages, colors, etc.)
├── data/
│   ├── daily_entries.csv  # Daily wellness entries
│   └── weekly_summaries.csv # Weekly summaries
├── templates/
│   └── base.html          # Main HTML template with all tabs
└── static/
    ├── css/
    │   └── style.css      # Dark theme styling
    └── js/
        ├── main.js        # Tab switching and API calls
        ├── daily_log.js   # Daily log interactions
        └── weekly_chart.js # Radar chart functionality
```

## API Endpoints

- `GET /` - Main page
- `GET /api/daily-log` - Get all daily entries
- `POST /api/daily-log` - Save a daily entry
- `GET /api/weekly-summary` - Get all weekly summaries
- `POST /api/weekly-summary` - Save a weekly summary
- `GET /api/weekly-averages/<date>` - Calculate weekly average for a specific date

## Tips for Using the Tracker

1. **Consistency**: Track daily for better pattern recognition
2. **Honesty**: Rate yourself objectively - these scores are for you
3. **Patterns**: Look for weekly patterns in your wellness shape
4. **Adjustments**: If you're low on energy or high on stress, investigate and adjust
5. **Career Signal**: Use Productivity as a personal career signal for burnout detection

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js (radar/polygon charts)
- **Data**: CSV files (simple, portable)
- **Theme**: Dark mode with accent colors

## License

MIT
