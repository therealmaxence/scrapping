from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
from logic import get_all_events, parse_date, save_local_event, get_ics_url, save_ics_url
import requests
import json

from utils.calendar_logic import (
    get_combined_events,
    load_calendar,
    save_calendar_url,
    calendar_url_exists,
    load_local_event,
    add_local_event,
)
from ics import Calendar
from dateutil import parser
import os

app = Flask(__name__)

# ----------------------------------------------------------
# Routes
# ----------------------------------------------------------

@app.route('/')
def home():
    if not calendar_url_exists():
        return render_template('upload_link.html')
    return redirect(url_for('index'))


@app.route('/set_calendar', methods=['POST'])
def set_calendar():
    url = request.form.get('calendar_url', '').strip()
    if not url.startswith("http"):
        return "❌ Please provide a valid HTTPS calendar link.", 400
    save_calendar_url(url)
    return redirect(url_for('index'))


@app.route('/calendar')
def index():
    return render_template('index.html')


@app.route("/events.json")
def events():
    start = parse_date(request.args.get("start"))
    end = parse_date(request.args.get("end"))
    return jsonify(get_all_events(start, end))


@app.route('/event/<event_id>')
def event_detail(event_id):
    try:
        # Load ICS URL
        url_file = "ics_calendar_viewer\\calendar_url.txt"
        ics_url = open(url_file).read().strip() if os.path.exists(url_file) else ""

        events = []

        # -----------------------------------------
        # Load ICS events (same as /events.json)
        # -----------------------------------------
        if ics_url:
            try:

                ics_data = requests.get(ics_url).text
                cal = Calendar(ics_data)
                for e in cal.events:
                    events.append(e)
            except Exception as e:
                print("ICS load error:", e)

        # -----------------------------------------
        # Load local events
        # -----------------------------------------
        local_file = "local_events.json"
        local_events = []

        if os.path.exists(local_file):
            local_events = json.load(open(local_file))

        # Try finding the event in ICS first
        ev = next((e for e in events if e.uid == event_id), None)

        # Try finding event in local events
        if not ev:
            local = next((x for x in local_events if x["id"] == event_id), None)
            if local:
                # convert to fake ICS-like object
                return render_template(
                    "event_detail.html",
                    event={
                        "title": local["title"],
                        "start": local["start"],
                        "end": local["end"],
                        "location": local.get("location",""),
                        "description": local.get("description",""),
                    },
                    prev_event=None,
                    next_event=None
                )

        if not ev:
            abort(404)

        # Build event data
        event_data = {
            "title": ev.name,
            "start": ev.begin.to('local').format("YYYY-MM-DD HH:mm"),
            "end": ev.end.to('local').format("YYYY-MM-DD HH:mm"),
            "location": ev.location or None,
            "description": ev.description or None,
        }

        # Sort to compute prev/next
        sorted_events = sorted(events, key=lambda e: e.begin)
        current_index = next(i for i, e in enumerate(sorted_events) if e.uid == event_id)

        return render_template(
            "event_detail.html",
            event=event_data,
            prev_event=sorted_events[current_index - 1].uid if current_index > 0 else None,
            next_event=sorted_events[current_index + 1].uid if current_index < len(sorted_events)-1 else None
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------------
# Add new event manually (saved locally)
# ----------------------------------------------------------
@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        save_local_event(
            request.form["title"],
            request.form["start"],
            request.form["end"],
            request.form.get("description", "")
        )
        return redirect("/")
    return render_template("add_event.html")


# ----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
