import unittest2 as unittest
from datetime import date
from icalendar import Calendar, Event


def get_ical(dates):
    cal = Calendar()
    for adate in dates:
        event = Event()
        event['dtstart'] = adate.strftime('%Y%m%dT113000')
        event['dtend'] = adate.strftime('%Y%m%dT200000')
        cal.add_component(event)
    return cal.to_ical()


class TestShiftcal(unittest.TestCase):
    def test_fixed_date(self):
        adate = date(2014, 1, 1)
        ical = get_ical([adate])
        self.assertEqual(
            ical.replace('\r\n', '\n').strip(),
            """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20140101T113000
DTEND:20140101T200000
END:VEVENT
END:VCALENDAR""")

if __name__ == '__main__':
    unittest.main()
