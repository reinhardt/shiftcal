from datetime import timedelta
from icalendar import Calendar, Event


OFF, EARLY, LATE, NIGHT, DOUBLE = (0, 1, 2, 3, 4)
DEFAULT_DEFINITIONS = {
    OFF: None,
    EARLY: ['080000', '160000'],
    LATE: ['113000', '200000'],
    NIGHT: ['203000', '074500'],
    DOUBLE: ['080000', '200000'],
}


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
