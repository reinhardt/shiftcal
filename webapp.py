import os
from ConfigParser import SafeConfigParser
from datetime import date
from datetime import datetime
from datetime import timedelta
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from urlparse import parse_qsl

from shiftcal import ShiftCal
from shiftcal import DEFAULT_DEFINITIONS
from shiftcal import get_definitions

app = Flask(__name__)


definitions = DEFAULT_DEFINITIONS
if os.path.exists('shiftcal.cfg'):
    config = SafeConfigParser()
    config.read('shiftcal.cfg')
    definitions = get_definitions(config)


@app.route("/")
def root():
    start_date = today = date.today()
    query = dict(parse_qsl(request.query_string))
    if 'start_date' in query:
        start_date = datetime.strptime(query['start_date'], '%Y-%m-%d').date()

    shifts = [
        {'token': d,
         'title': definitions[d].get('title', d).decode('utf-8'),
         'checked': ''}
        for d in definitions]
    shifts[0]['checked'] = 'checked="checked"'
    num_dates = int(query.get('num_dates', 7))
    num_more_dates = int(query.get('num_more_dates', 7))
    if 'num_dates' in query:
        if 'more' in query:
            num_dates += num_more_dates
        if 'less' in query:
            num_dates -= num_more_dates
            if num_dates < 0:
                num_dates = 1
    dates = [start_date + timedelta(days) for days in range(num_dates)]
    return render_template(
        'shiftcal.html',
        shifts=shifts, start_date=start_date, dates=dates, num_dates=num_dates,
        num_more_dates=num_more_dates)


@app.route("/shiftcal.ics")
def ical():
    start_date = today = date.today()
    query = dict(parse_qsl(request.query_string))
    if 'start_date' in query:
        start_date = datetime.strptime(query['start_date'], '%Y-%m-%d').date()
    shifts = ''.join([query[key] for key in sorted(query)
                     if key.startswith('shift-')])
    shiftcal = ShiftCal(start_date, shifts, definitions=definitions)
    ical = shiftcal.get_ical()
    resp = make_response(ical)
    resp.headers['Content-Type'] = 'text/calendar'
    resp.headers['Content-Disposition'] = 'inline'
    resp.headers['Content-Length'] = len(ical)
    return resp

if __name__ == "__main__":
    app.run(debug=True)
