from flask import Flask, jsonify,send_from_directory, url_for, render_template, abort
from ics import Calendar
import os
from dateutil import parser
from flask import request

app = Flask(__name__)

@app.route('/calendar')
def index():
    return send_from_directory('.', 'templates/index.html')

from dateutil import parser

@app.route('/events.json')
def get_events():
    try:
        start_str = request.args.get('start')
        end_str = request.args.get('end')
        
        start_date = parser.parse(start_str) if start_str else None
        end_date = parser.parse(end_str) if end_str else None
        
        path = os.path.join(os.path.dirname(__file__), "templates/emploi_du_temps.ics")
        with open(path, "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())
        
        filtered_events = []
        for event in calendar.events:
            event_start = event.begin.datetime
            event_end = event.end.datetime
            
            if ((not start_date or event_end >= start_date) and 
                (not end_date or event_start <= end_date)):
                filtered_events.append({
                    'id': event.uid,
                    'title': event.name,
                    'start': event_start.isoformat(),
                    'end': event_end.isoformat(),
                    'location': event.location,
                    'description': event.description
                })
        
        return jsonify(filtered_events)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/event/<event_id>')
def event_detail(event_id):
    try:
        path = os.path.join(os.path.dirname(__file__), "templates/emploi_du_temps.ics")
        with open(path, "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())

        ev = next((e for e in calendar.events if e.uid == event_id), None)
        if not ev:
            abort(404)

        event_data = {
            "title":       ev.name,
            "start":       ev.begin.to('local').format("YYYY-MM-DD HH:mm"),
            "end":         ev.end.to('local').format("YYYY-MM-DD HH:mm"),
            "location":    ev.location or None,
            "description": ev.description or None,
        }
    
        sorted_events = sorted(calendar.events, key=lambda e: e.begin)
        current_index = next(i for i, e in enumerate(sorted_events) if e.uid == event_id)
        
        return render_template("event_detail.html",
            event=event_data,
            prev_event=sorted_events[current_index-1].uid if current_index > 0 else None,
            next_event=sorted_events[current_index+1].uid if current_index < len(sorted_events)-1 else None
        )
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
