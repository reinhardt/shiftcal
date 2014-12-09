Shiftcal
========

Shiftcal is a script that generates ical data from a shift plan.

Usage
-----

The shift plan is represented as a string of letters representing consecutive days. Every letter stands for a specific shift, e.g. E for early shift. A sample call would be

    $ python shiftcal.py EEE > test.ics

This generates an ical file test.ics containing three consecutive days of early shifts, starting today. To start from a different date, use the --startdate parameter:

    $ python shiftcal.py --startdate 20141103 EEE > test.ics

The format for the start date is YYYYMMDD (four digits for the year, then two difits each for month and day).

There is also a flask app. If you have installed flask you can run it with

    $ python webapp.py

Configuration
-------------

The default shifts are defined in shiftcal_defaults.cfg. To override them, create a file shiftcal.cfg. In the [shiftcal] section there has to be one configuration option, "shifts". It must contain a comma separated list of shifts that you want to define. For each shift you then create another section of the same name, containing at least the option "token". For example:

    [shiftcal]
    shifts = early, late

    [early]
    token = E
    title = Early shift
    start = 0730
    end = 1530

    [late]
    ...

The token must be a single character. It is what you use on the command line to refer to this shift.

"start" and "end" define the beginning and end times of the shift, using the format HHMM (two digits each for hour and minute). If you do not add start or end, the token will be interpreted as a day off; i.e. every day in the shift plan that has the respective token will be skipped in the ical data.

"title" is optional but recommended. It will be visible as the event summary in the ical data.
