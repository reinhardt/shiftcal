import argparse
import os
import re
from ConfigParser import SafeConfigParser
from datetime import date
from datetime import datetime
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
        start = pad_time(config.get(shift, 'start'))
        end = pad_time(config.get(shift, 'end'))
        shiftdata[token] = [start, end]
    return shiftdata


OFF, EARLY, LATE, NIGHT, DOUBLE = ('O', 'E', 'L', 'N', 'D')
default_config = SafeConfigParser()
default_config.read('shiftcal_defaults.cfg')
DEFAULT_DEFINITIONS = get_definitions(default_config)
DEFAULT_DEFINITIONS[OFF] = None


class ShiftCal(object):
    def __init__(self, start_date, shifts, definitions=[]):
        self.start_date = start_date
        self.shifts = shifts
        self.definitions = definitions or DEFAULT_DEFINITIONS

    def get_ical(self):
        cal = Calendar()
        adate = self.start_date
        for shift in self.shifts:
            event = Event()
            if shift not in self.definitions:
                print('Unknown shift: {}'.format(shift))
                times = None
            else:
                times = self.definitions[shift]
            if times is not None:
                event['dtstart'] = adate.strftime(
                    '%Y%m%dT{0}'.format(times[0]))
                if int(times[0]) > int(times[1]):
                    enddate = adate + timedelta(1)
                else:
                    enddate = adate
                event['dtend'] = enddate.strftime(
                    '%Y%m%dT{0}'.format(times[1]))

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
        else:
            print('error: unrecognized startdate format: {0}'.format(
                args.startdate))
            exit(1)

    shiftcal = ShiftCal(start_date, args.shifts, definitions=definitions)
    print(shiftcal.get_ical())
