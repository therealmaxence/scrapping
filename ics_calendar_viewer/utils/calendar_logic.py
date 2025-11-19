import os
import time
import requests
import json
from ics import Calendar
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
URL_PATH = os.path.join(BASE_DIR, "templates/calendar_url.txt")
EVENTS_PATH = os.path.join(BASE_DIR, "templates/local_events.json")

CACHE = {"calendar": None, "timestamp": 0, "url": None}
CACHE_DURATION = 600  # 10 minutes


# ----------------------------------------------------------
# Calendar logic
# ----------------------------------------------------------
def calendar_url_exists():
    return os.path.exists(URL_PATH)


def save_calendar_url(url):
    with open(URL_PATH, 'w', encoding='utf-8') as f:
        f.write(url)
    CACHE.update({"calendar": None, "timestamp": 0, "url": url})


def load_calendar():
    """Load calendar from remote ICS URL (with caching)"""
    if not os.path.exists(URL_PATH):
        raise FileNotFoundError("Calendar URL not set.")
    with open(URL_PATH, 'r', encoding='utf-8') as f:
        url = f.read().strip()

    now = time.time()
    if CACHE["calendar"] and CACHE["url"] == url and (now - CACHE["timestamp"] < CACHE_DURATION):
        return CACHE["calendar"]

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    calendar = Calendar(response.text)

    CACHE.update({"calendar": calendar, "timestamp": now, "url": url})
    return calendar


# ----------------------------------------------------------
# Local events logic
# ----------------------------------------------------------
def _load_local_events():
    if not os.path.exists(EVENTS_PATH):
        return []
    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_local_events(events):
    with open(EVENTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)


def add_local_event(title, start, end, location, description):
    events = _load_local_events()
    event = {
        "id": str(uuid.uuid4()),
        "title": title,
        "start": start,
        "end": end,
        "location": location,
        "description": description,
        "source": "local"
    }
    events.append(event)
    _save_local_events(events)


def load_local_event(event_id):
    events = _load_local_events()
    return next((e for e in events if e["id"] == event_id), None)


# ----------------------------------------------------------
# Combine ICS + local events
# ----------------------------------------------------------
def get_combined_events(start_date=None, end_date=None):
    """Return events from ICS + locally added events"""
    events = []

    # Remote events
    try:
        calendar = load_calendar()
        for e in calendar.events:
            event_start = e.begin.datetime
            event_end = e.end.datetime
            if ((not start_date or event_end >= start_date) and
                (not end_date or event_start <= end_date)):
                events.append({
                    "id": e.uid,
                    "title": e.name,
                    "start": event_start.isoformat(),
                    "end": event_end.isoformat(),
                    "location": e.location,
                    "description": e.description,
                    "source": "ics"
                })
    except Exception:
        pass  # ignore if ICS not reachable

    # Local events
    local_events = _load_local_events()
    for ev in local_events:
        ev_start = parser.parse(ev["start"])
        ev_end = parser.parse(ev["end"])
        if ((not start_date or ev_end >= start_date) and
            (not end_date or ev_start <= end_date)):
            events.append(ev)

    return events
