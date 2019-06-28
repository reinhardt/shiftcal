from __future__ import print_function
import argparse
import os
import pytz
import re
import sys
from ConfigParser import SafeConfigParser
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from icalendar import Calendar, Event


def pad_time(timestr):
    if len(timestr) == 4:
        timestr += '00'
    return timestr


def get_definitions(config):
    shifts = config.get('shiftcal', 'shifts').split(',')
    shiftdata = {}
    for shift in shifts:
        shift = shift.strip()
        token = config.get(shift, 'token')
        shiftdata[token] = {}
        if (config.has_option(shift, 'start') and
                config.has_option(shift, 'end')):
            start = pad_time(config.get(shift, 'start'))
            end = pad_time(config.get(shift, 'end'))
            shiftdata[token].update({
                'start': start,
                'end': end,
            })
        if config.has_option(shift, 'title'):
            shiftdata[token]['title'] = config.get(shift, 'title')
    return shiftdata


OFF, EARLY, LATE, NIGHT, DOUBLE = ('O', 'E', 'L', 'N', 'D')
default_config = SafeConfigParser()
default_config.read('shiftcal_defaults.cfg')
DEFAULT_DEFINITIONS = get_definitions(default_config)
DEFAULT_DEFINITIONS[OFF] = None


class ShiftCal(object):
    def __init__(self, start_date, shifts, definitions=[], timezone=None):
        self.start_date = start_date
        self.shifts = shifts
        self.definitions = definitions or DEFAULT_DEFINITIONS
        self.timezone = timezone

    def get_ical(self):
        cal = Calendar()
        adate = self.start_date
        for shift in self.shifts:
            event = Event()
            if shift not in self.definitions:
                print('WARNING: Unknown shift: {}'.format(shift),
                      file=sys.stderr)
                times = None
            else:
                if self.definitions[shift]:
                    times = [self.definitions[shift]['start'],
                             self.definitions[shift]['end']]
                else:
                    times = None
            if times is not None:
                starttime = time(int(times[0][:2]), int(times[0][2:4]),
                                 tzinfo=self.timezone)
                event.add('dtstart', datetime.combine(adate, starttime))
                if int(times[0]) > int(times[1]):
                    enddate = adate + timedelta(1)
                else:
                    enddate = adate
                endtime = time(int(times[1][:2]), int(times[1][2:4]),
                               tzinfo=self.timezone)
                event.add('dtend', datetime.combine(enddate, endtime))
                if 'title' in self.definitions[shift]:
                    event['summary'] = self.definitions[shift]['title']

                cal.add_component(event)
            adate += timedelta(1)
        return cal.to_ical()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate ical shift calendars')
    parser.add_argument(
        '--startdate',
        type=str,
        help='the start date for the shift plan, in format YYYYMMDD'
        ' or as an offset in days from today, e.g. -1 for yesterday')
    parser.add_argument(
        '--timezone',
        type=str,
        help='a string representation of the time zone to use')
    parser.add_argument(
        'shifts',
        type=str,
        help='a string describing the shift plan, e.g. EENDNOL')
    args = parser.parse_args()

    definitions = None
    if os.path.exists('shiftcal.cfg'):
        config = SafeConfigParser()
        config.read('shiftcal.cfg')
        definitions = get_definitions(config)

    start_date = today = date.today()
    if args.startdate:
        if args.startdate == 'today':
            start_date = today
        elif re.match(r'[+-][0-9]*$', args.startdate):
            start_date = today + timedelta(int(args.startdate))
        elif re.match(r'[0-9]{8}$', args.startdate):
            start_date = datetime.strptime(args.startdate, '%Y%m%d')
        elif re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}$', args.startdate):
            start_date = datetime.strptime(args.startdate, '%Y-%m-%d')
        else:
            print('ERROR: unrecognized startdate format: {0}'.format(
                args.startdate), file=sys.stderr)
            exit(1)

    if args.timezone:
        timezone = pytz.timezone(args.timezone)
    else:
        timezone = None

    shiftcal = ShiftCal(start_date, args.shifts, definitions=definitions,
                        timezone=timezone)
    print(shiftcal.get_ical())
