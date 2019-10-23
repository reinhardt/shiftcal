import unittest
from configparser import ConfigParser
from datetime import date
from io import StringIO
import pytz

from shiftcal import ShiftCal
from shiftcal import OFF
from shiftcal import EARLY
from shiftcal import LATE
from shiftcal import NIGHT
from shiftcal import DOUBLE
from shiftcal import default_config
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
DTSTART;VALUE=DATE-TIME:20140101T113000
DTEND;VALUE=DATE-TIME:20140101T200000
END:VEVENT
END:VCALENDAR""")

    def test_single_date_late_shift_with_title(self):
        definitions = get_definitions(default_config)
        definitions['L']['title'] = 'Late'
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [LATE], definitions=definitions)
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
SUMMARY:Late
DTSTART;VALUE=DATE-TIME:20140101T113000
DTEND;VALUE=DATE-TIME:20140101T200000
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
DTSTART;VALUE=DATE-TIME:20140101T080000
DTEND;VALUE=DATE-TIME:20140101T160000
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
DTSTART;VALUE=DATE-TIME:20140101T203000
DTEND;VALUE=DATE-TIME:20140102T074500
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
DTSTART;VALUE=DATE-TIME:20140101T080000
DTEND;VALUE=DATE-TIME:20140101T200000
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
DTSTART;VALUE=DATE-TIME:20140101T080000
DTEND;VALUE=DATE-TIME:20140101T160000
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE-TIME:20140102T080000
DTEND;VALUE=DATE-TIME:20140102T160000
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
DTSTART;VALUE=DATE-TIME:20140728T080000
DTEND;VALUE=DATE-TIME:20140728T160000
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE-TIME:20140729T080000
DTEND;VALUE=DATE-TIME:20140729T160000
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE-TIME:20140801T113000
DTEND;VALUE=DATE-TIME:20140801T200000
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE-TIME:20140802T080000
DTEND;VALUE=DATE-TIME:20140802T160000
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE-TIME:20140803T080000
DTEND;VALUE=DATE-TIME:20140803T160000
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE-TIME:20140804T113000
DTEND;VALUE=DATE-TIME:20140804T200000
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
DTSTART;VALUE=DATE-TIME:20140728T080000
DTEND;VALUE=DATE-TIME:20140728T160000
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE-TIME:20140730T113000
DTEND;VALUE=DATE-TIME:20140730T200000
END:VEVENT
END:VCALENDAR""")

    def test_timezone(self):
        adate = date(2014, 1, 1)
        shiftcal = ShiftCal(adate, [LATE],
                            timezone=pytz.timezone("Europe/Berlin"))
        ical = shiftcal.get_ical()
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART;TZID=Europe/Berlin;VALUE=DATE-TIME:20140101T113000
DTEND;TZID=Europe/Berlin;VALUE=DATE-TIME:20140101T200000
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
        config_parser = ConfigParser()
        config_parser.read_file(StringIO(config))
        definitions = get_definitions(config_parser)
        self.assertIn('E', definitions)
        self.assertEqual(definitions['E']['start'], '073000')
        self.assertEqual(definitions['E']['end'], '153000')

    def test_early_shift_with_title(self):
        config = u"""[shiftcal]
shifts = early

[early]
token = E
title = Early
start = 0730
end = 1530"""
        config_parser = ConfigParser()
        config_parser.read_file(StringIO(config))
        definitions = get_definitions(config_parser)
        self.assertIn('E', definitions)
        self.assertEqual(definitions['E']['start'], '073000')
        self.assertEqual(definitions['E']['end'], '153000')
        self.assertEqual(definitions['E']['title'], 'Early')

    def test_late_shift(self):
        config = u"""[shiftcal]
shifts = late

[late]
token = L
start = 1300
end = 2100"""
        config_parser = ConfigParser()
        config_parser.read_file(StringIO(config))
        definitions = get_definitions(config_parser)
        self.assertIn('L', definitions)
        self.assertEqual(definitions['L']['start'], '130000')
        self.assertEqual(definitions['L']['end'], '210000')

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
        config_parser = ConfigParser()
        config_parser.read_file(StringIO(config))
        definitions = get_definitions(config_parser)
        self.assertIn('E', definitions)
        self.assertEqual(definitions['E']['start'], '073000')
        self.assertEqual(definitions['E']['end'], '153000')
        self.assertIn('N', definitions)
        self.assertEqual(definitions['N']['start'], '203000')
        self.assertEqual(definitions['N']['end'], '074500')

    def test_off(self):
        config = u"""[shiftcal]
shifts = off

[off]
token = O"""
        config_parser = ConfigParser()
        config_parser.read_file(StringIO(config))
        definitions = get_definitions(config_parser)
        self.assertIn('O', definitions)
        self.assertNotIn('start', definitions['O'])
        self.assertNotIn('end', definitions['O'])


if __name__ == '__main__':
    unittest.main()
