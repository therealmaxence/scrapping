import os
import json
import requests
from datetime import datetime
from dateutil import parser
from ics import Calendar
import uuid

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICS_URL_FILE = os.path.join(BASE_DIR, "calendar_url.txt")
LOCAL_EVENTS_FILE = os.path.join(BASE_DIR, "local_events.json")


# ---------------------------------------------------------
# ICS URL MANAGEMENT
# ---------------------------------------------------------

def get_ics_url():
    """Return the saved ICS URL, or an empty string if missing."""
    if not os.path.exists(ICS_URL_FILE):
        return ""
    with open(ICS_URL_FILE, "r") as f:
        return f.read().strip()


def save_ics_url(url: str):
    """Save or update the ICS URL."""
    with open(ICS_URL_FILE, "w") as f:
        f.write(url.strip())


# ---------------------------------------------------------
# ICS EVENTS
# ---------------------------------------------------------

def load_ics_events(start_date=None, end_date=None):
    """Download ICS file from URL and return a list of events."""
    url = get_ics_url()
    if not url:
        return []  # No ICS set yet

    try:
        response = requests.get(url)
        response.raise_for_status()
        ics_data = response.text
        cal = Calendar(ics_data)
    except Exception as e:
        print("ICS Loading Error:", e)
        return []

    events = []
    for ev in cal.events:
        ev_start = ev.begin.datetime
        ev_end = ev.end.datetime

        # Filtering with FullCalendar dates
        if start_date and ev_end < start_date:
            continue
        if end_date and ev_start > end_date:
            continue

        events.append({
            "id": ev.uid,
            "title": get_readable_name(ev.name),
            "start": ev_start.isoformat(),
            "end": ev_end.isoformat(),
            "location": ev.location,
            "description": ev.description,
            "source": "ics",
            "backgroundColor": get_color(ev.name)
        })

    return events


# ---------------------------------------------------------
# LOCAL EVENTS (SAVED MANUALLY)
# ---------------------------------------------------------

def load_local_events():
    """Load custom events saved locally."""
    if not os.path.exists(LOCAL_EVENTS_FILE):
        return []

    try:
        with open(LOCAL_EVENTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_local_event(title, start, end, description="", location=""):
    """Add a new local event."""
    events = load_local_events()

    new_event = {
        "id": f"local-{uuid.uuid4()}",
        "title": title,
        "start": start,
        "end": end,
        "description": description,
        "location": location,
        "source": "local",
        "backgroundColor": "#22c55e"  # green
    }

    events.append(new_event)

    with open(LOCAL_EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=2)

    return new_event


# ---------------------------------------------------------
# MERGE EVENTS
# ---------------------------------------------------------

def get_all_events(start_date=None, end_date=None):
    """Return all events, merging ICS + local ones."""
    ics_events = load_ics_events(start_date, end_date)
    local_events = load_local_events()

    # Local events are not filtered — user-created events always show
    return ics_events + local_events


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def parse_date(date_str):
    """Convert a date string to datetime, or None."""
    return parser.parse(date_str) if date_str else None


# ---------------------------------------------------------
# Name color rules
# ---------------------------------------------------------

COLOR_RULES = [
    ("CM", "#ef4444"),
    ("TD", "#2f8348"),
    ("TP", "#dcda53"),
    ("EX", "#3b82f6"),
    ("Proj", "#533f86")
]

def get_readable_name(name: str) -> str:
    """Return a more readable name by removing keywords."""
    readable_name = name.replace("_"," ").split()
    return readable_name[0]

def get_color(name: str) -> str:
    for keyword, color in COLOR_RULES:
        if keyword in name:
            return color
    return "#6b7280"  # default gray
