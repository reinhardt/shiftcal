import unittest2 as unittest
from ConfigParser import SafeConfigParser
from datetime import date
from io import StringIO

from shiftcal import ShiftCal
from shiftcal import OFF
from shiftcal import EARLY
from shiftcal import LATE
from shiftcal import NIGHT
from shiftcal import DOUBLE
from shiftcal import get_definitions


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


class TestConfig(unittest.TestCase):
    def test_early_shift(self):
        config = u"""[shiftcal]
shifts = early

[early]
token = E
start = 0730
end = 1530"""
        config_parser = SafeConfigParser()
        config_parser.readfp(StringIO(unicode(config)))
        definitions = get_definitions(config_parser)
        self.assertIn('E', definitions)
        self.assertEqual(definitions['E'][0], '073000')
        self.assertEqual(definitions['E'][1], '153000')

    def test_late_shift(self):
        config = u"""[shiftcal]
shifts = late

[late]
token = L
start = 1300
end = 2100"""
        config_parser = SafeConfigParser()
        config_parser.readfp(StringIO(unicode(config)))
        definitions = get_definitions(config_parser)
        self.assertIn('L', definitions)
        self.assertEqual(definitions['L'][0], '130000')
        self.assertEqual(definitions['L'][1], '210000')

    def test_early_and_night_shift(self):
        config = u"""[shiftcal]
shifts = early, night

[early]
token = E
start = 0730
end = 1530

[night]
token = N
start = 2030
end = 0745"""
        config_parser = SafeConfigParser()
        config_parser.readfp(StringIO(unicode(config)))
        definitions = get_definitions(config_parser)
        self.assertIn('E', definitions)
        self.assertEqual(definitions['E'][0], '073000')
        self.assertEqual(definitions['E'][1], '153000')
        self.assertIn('N', definitions)
        self.assertEqual(definitions['N'][0], '203000')
        self.assertEqual(definitions['N'][1], '074500')

if __name__ == '__main__':
    unittest.main()
