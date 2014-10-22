import unittest2 as unittest
from datetime import date
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


class TestShiftcal(unittest.TestCase):
    def test_single_date_late_shift(self):
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [LATE])
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140101T113000
DTEND:20140101T200000
END:VEVENT
END:VCALENDAR""")

    def test_single_date_early_shift(self):
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [EARLY])
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140101T080000
DTEND:20140101T160000
END:VEVENT
END:VCALENDAR""")

    def test_single_date_night_shift(self):
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [NIGHT])
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140101T203000
DTEND:20140102T074500
END:VEVENT
END:VCALENDAR""")

    def test_single_date_double_shift(self):
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [DOUBLE])
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140101T080000
DTEND:20140101T200000
END:VEVENT
END:VCALENDAR""")

    def test_single_date_off(self):
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [OFF])
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
END:VCALENDAR""")

    def test_two_early_shifts(self):
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [EARLY, EARLY])
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140101T080000
DTEND:20140101T160000
END:VEVENT
BEGIN:VEVENT
DTSTART:20140102T080000
DTEND:20140102T160000
END:VEVENT
END:VCALENDAR""")

    def test_realistic_shifts(self):
        adate = date(2014, 7, 28)
        shiftcal = ShiftCal(
            adate,
            [EARLY, EARLY, OFF, OFF, LATE, EARLY, EARLY, LATE])
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140728T080000
DTEND:20140728T160000
END:VEVENT
BEGIN:VEVENT
DTSTART:20140729T080000
DTEND:20140729T160000
END:VEVENT
BEGIN:VEVENT
DTSTART:20140801T113000
DTEND:20140801T200000
END:VEVENT
BEGIN:VEVENT
DTSTART:20140802T080000
DTEND:20140802T160000
END:VEVENT
BEGIN:VEVENT
DTSTART:20140803T080000
DTEND:20140803T160000
END:VEVENT
BEGIN:VEVENT
DTSTART:20140804T113000
DTEND:20140804T200000
END:VEVENT
END:VCALENDAR""")

if __name__ == '__main__':
    unittest.main()
