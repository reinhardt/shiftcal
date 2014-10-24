import unittest2 as unittest
from datetime import date

from shiftcal import ShiftCal
from shiftcal import OFF
from shiftcal import EARLY
from shiftcal import LATE
from shiftcal import NIGHT
from shiftcal import DOUBLE


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

    def test_shifts_string(self):
        adate = date(2014, 7, 28)
        shiftcal = ShiftCal(
            adate,
            'EOL')
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140728T080000
DTEND:20140728T160000
END:VEVENT
BEGIN:VEVENT
DTSTART:20140730T113000
DTEND:20140730T200000
END:VEVENT
END:VCALENDAR""")

if __name__ == '__main__':
    unittest.main()

