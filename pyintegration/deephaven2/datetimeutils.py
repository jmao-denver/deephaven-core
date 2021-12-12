#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
""" Utilities for Deephaven date/time storage and manipulation."""

import jpy

from deephaven2 import DHError
from deephaven2.dtypes import DateTime, Period, DType
from deephaven2.constants import TimeZone

SECOND = 1000000000  #: One second in nanoseconds.
MINUTE = 60 * SECOND  #: One minute in nanoseconds.
HOUR = 60 * MINUTE  #: One hour in nanoseconds.
DAY = 24 * HOUR  #: One day in nanoseconds.
WEEK = 7 * DAY  #: One week in nanoseconds.
YEAR = 52 * WEEK  #: One year in nanoseconds.

_JDateTimeUtils = jpy.get_type("io.deephaven.time.DateTimeUtils")


def convert_datetime(s: str, quiet: bool = False) -> DateTime:
    """ Converts a datetime string from a few specific zoned formats to a DateTime object

    Args:
        s (str): usually in the form yyyy-MM-ddThh:mm:ss and with optional sub-seconds after an
            optional decimal point, followed by a mandatory time zone character code
        quiet (bool): to return None or raise an exception if the string can't be parsed, default is False

    Returns:
        a DateTime

    Raises:
        DHError
    """
    if quiet:
        return DateTime(_JDateTimeUtils.convertDateTimeQuiet(s))

    try:
        return DateTime(_JDateTimeUtils.convertDateTime(s))
    except Exception as e:
        raise DHError(e) from e


def convert_period(s: str, quiet: bool = False) -> Period:
    """ Converts a period string into a Period object.

    Args:
        s (str): in the form of number+type, e.g. 1W for one week, or T+number+type, e.g. T1M for one minute
        quiet (bool): to return None or raise an exception if the string can't be parsed, default is False

    Returns:
        Period

    Raises:
        DHError
    """
    if quiet:
        return Period(_JDateTimeUtils.convertPeriodQuiet(s))

    try:
        return Period(_JDateTimeUtils.convertPeriod(s))
    except Exception as e:
        raise DHError(e) from e


def convert_time(s, quiet: bool = False) -> int:
    """ Converts a string time to nanoseconds from Epoch.

    Args:
        s (str): in the format of: hh:mm:ss[.nnnnnnnnn]
        quiet (bool): to return None or raise an exception if the string can't be parsed, default is False

    Returns:
        int

    Raises:
        DHError
    """
    if quiet:
        return _JDateTimeUtils.convertTimeQuiet(s)

    try:
        return _JDateTimeUtils.convertTime(s)
    except Exception as e:
        raise DHError(e) from e


def current_time() -> DateTime:
    """ Provides the current date/time, or, if a custom timeProvider has been configured, provides the current
     time according to the custom provider.

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return DateTime(_JDateTimeUtils.currentTime())
    except Exception as e:
        raise DHError(e) from e


def date_at_midnight(dt: DateTime, tz: TimeZone) -> DateTime:
    """ Returns a DateTime for the requested DateTime at midnight in the specified time zone.

    Args:
        dt (DateTime) - DateTime for which the new value at midnight should be calculated
        tz: (TimeZone) - TimeZone for which the new value at midnight should be calculated

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return DateTime(_JDateTimeUtils.dateAtMidnight(dt.j_datetime, tz.value))
    except Exception as e:
        raise DHError(e) from e


def day_of_month(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of the day of the month for a DateTime and specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the day of the month
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.dateOfMonth(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def day_of_week(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of the day of the week for a DateTime in the specified time zone, with 1 being
     Monday and 7 being Sunday.

    Args:
        dt (DateTime): the DateTime for which to find the day of the week.
        tz (TimeZone): the TimeZone to use when interpreting the date/time.

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.dateOfWeek(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def day_of_year(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of the day of the year (Julian date) for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the day of the year
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.dateOfYear(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def diff_nanos(dt1: DateTime, dt2: DateTime) -> int:
    """ Returns the difference in nanoseconds between two DateTime values.

    Args:
        dt1 (DateTime): the 1st DateTime
        dt2 (DateTime): the 2nd DateTime

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.diffNanos(dt1.j_datetime, dt2.j_datetime)
    except Exception as e:
        raise DHError(e) from e


def format(dt: DateTime, tz: TimeZone) -> str:
    """ Returns a string date/time representation formatted as yyyy-MM-ddThh:mm:ss.nnnnnnnnn TZ.

    Args:
        dt (DateTime): the DateTime to format as a string
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        str

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.format(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def format_nanos(ns: int) -> str:
    """ Returns a string date/time representation formatted as yyyy-MM-ddThh:mm:ss.nnnnnnnnn TZ.

    Args:
        ns (int): the number of nanoseconds from Epoch

    Returns:
        str

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.format(ns)
    except Exception as e:
        raise DHError(e) from e


def format_as_date(dt: DateTime, tz: TimeZone) -> str:
    """ Returns a string date representation of a DateTime interpreted for a specified time zone formatted as yyy-MM-dd.

    Args:
        dt (DateTime): the DateTime to format
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        str

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.formatDate(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def hour_of_day(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of the hour of the day for a DateTime in the specified time zone. The hour is on a
     24 hour clock (0 - 23).

    Args:
        dt (DateTime): the DateTime for which to find the hour of the day
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.hourOfDay(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def is_after(dt1: DateTime, dt2: DateTime) -> bool:
    """ Evaluates whether one DateTime value is later than a second DateTime value.

    Args:
        dt1 (DateTime): the 1st DateTime
        dt2 (DateTime): the 2nd DateTime

    Returns:
        bool

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.isAfter(dt1, dt2)
    except Exception as e:
        raise DHError(e) from e


def is_before(dt1: DateTime, dt2: DateTime) -> bool:
    """ Evaluates whether one DateTime value is later than a second DateTime value.

    Args:
        dt1 (DateTime): the 1st DateTime
        dt2 (DateTime): the 2nd DateTime

    Returns:
        bool

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.isBefore(dt1, dt2)
    except Exception as e:
        raise DHError(e) from e


def lower_bin(dt: DateTime, interval: int, offset: int = 0) -> DateTime:
    """ Returns a DateTime value, which is at the starting (lower) end of a time range defined by the interval
     nanoseconds. For example, a 5*MINUTE intervalNanos value would return the date/time value for the start of the
     five minute window that contains the input date time.

    Args:
        dt (DateTime): the DateTime for which to evaluate the start of the containing window
        interval (int): the size of the window in nanoseconds
        offset (int): the window start offset in nanoseconds. For example, a value of MINUTE would offset all windows by
              one minute. Default is 0

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.lowerBin(dt, interval, offset)
    except Exception as e:
        raise DHError(e) from e


def millis(dt: DateTime) -> int:
    """ Returns milliseconds since Epoch for a DateTime value.

    Args:
        dt (DateTime): the DateTime for which the milliseconds offset should be returned

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.millis(dt)
    except Exception as e:
        raise DHError(e) from e


def millis_of_day(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of milliseconds since midnight for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the milliseconds since midnight
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.millisOfDay(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def millis_of_second(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of milliseconds since the top of the second for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the milliseconds
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.millisOfSecond(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def millis_to_nanos(ms: int) -> int:
    """ Converts milliseconds to nanoseconds.

    Args:
        ms (int): the milliseconds value to convert

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.millisToNanos(ms)
    except Exception as e:
        raise DHError(e) from e


def millis_to_time(ms: int) -> DateTime:
    """ Converts a value of milliseconds from Epoch in the UTC time zone to a DateTime.

    Args:
        ms (int): the milliseconds value to convert

    returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.millisToTime(ms)
    except Exception as e:
        raise DHError(e) from e


def minus(dt1: DateTime, dt2: DateTime) -> int:
    """ Subtracts one time from another.

    Args:
        dt1 (DateTime): the 1st DateTime
        dt2 (DateTiem): the 2nd DateTime

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.minus(dt1, dt2)
    except Exception as e:
        raise DHError(e) from e


def minus_nanos(dt: DateTime, ns: int) -> DateTime:
    """ Subtracts nanoseconds from a DateTime.

    Args:
        dt (DateTime): the starting DateTime value
        ns (int): the long number of nanoseconds to subtract from dateTime

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.minus(dt, ns)
    except Exception as e:
        raise DHError(e) from e


def minus_period(dt: DateTime, period: Period) -> DateTime:
    """ Subtracts a period from a DateTime.

    Args:
        dt (DateTime): the starting DateTime value
        period (Period): the Period to subtract from dateTime

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.minus(dt, period)
    except Exception as e:
        raise DHError(e) from e


def minute_of_day(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of minutes since midnight for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the minutes
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.minuteOfDay(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def minute_of_hour(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of minutes since the top of the hour for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the minutes
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.minuteOfHour(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def month_of_year(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value for the month of a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the month
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.monthOfYear(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def nanos(dt: DateTime) -> int:
    """ Returns nanoseconds since Epoch for a DateTime value.

    Args:
        dt (DateTime): the DateTime for which the nanoseconds offset should be returned

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.nanos(dt)
    except Exception as e:
        raise DHError(e) from e


def nanos_of_day(dt: DateTime, tz: TimeZone) -> int:
    """ Returns a long value of nanoseconds since midnight for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the nanoseconds since midnight
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.nanosOfDay(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def nanos_of_second(dt: DateTime, tz: TimeZone) -> int:
    """ Returns a long value of nanoseconds since the top of the second for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the nanoseconds
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.nanosOfSecond(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def nanos_to_millis(ns: int) -> int:
    """ Converts nanoseconds to milliseconds.

    Args:
        ns (int): the value of nanoseconds to convert

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.nanosToMillis(ns)
    except Exception as e:
        raise DHError(e) from e


def nanos_to_time(ns: int) -> DateTime:
    """ Converts a value of nanoseconds from Epoch to a DateTime.

    Args:
        ns (long): the long nanoseconds since Epoch value to convert

    Returns:
        DateTime
    """
    try:
        return _JDateTimeUtils.nanosToTime(ns)
    except Exception as e:
        raise DHError(e) from e


def plus(dt: DateTime, period: Period) -> DateTime:
    """ Adds one time from another.

    Args:
        dt (DateTime): the starting DateTime value
        period (Period): the Period to add to the DateTime

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.plus(dt, period)
    except Exception as e:
        raise DHError(e) from e


def plus_nanos(ns: int) -> DateTime:
    """ Adds nanoseconds to a DateTime.

    Args:
        dt (DateTime): the starting DateTime value
        ns (int): the long number of nanoseconds to add to DateTime

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.plus(ns)
    except Exception as e:
        raise DHError(e) from e


def second_of_day(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of seconds since midnight for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the seconds
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.secondOfDay(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def second_of_minute(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of seconds since the top of the minute for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the seconds
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.secondOfMinute(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def upper_bin(dt: DateTime, interval: int, offset: int = 0) -> DateTime:
    """ Returns a DateTime value, which is at the ending (upper) end of a time range defined by the interval
     nanoseconds. For example, a 5*MINUTE intervalNanos value would return the date/time value for the end of the five
     minute window that contains the input date time.

    Args:
        dt (DateTime): the DateTime for which to evaluate the end of the containing window
        interval (int): the size of the window in nanoseconds
        offset (int): the window start offset in nanoseconds. For example, a value of MINUTE would offset all windows by
              one minute. Default is 0

    Returns:
        DateTime

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.upperBin(dt, interval, offset)
    except Exception as e:
        raise DHError(e) from e


def year(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of the year for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the year
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.year(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e


def year_of_century(dt: DateTime, tz: TimeZone) -> int:
    """ Returns an int value of the two-digit year for a DateTime in the specified time zone.

    Args:
        dt (DateTime): the DateTime for which to find the year
        tz (TimeZone): the TimeZone to use when interpreting the date/time

    Returns:
        int

    Raises:
        DHError
    """
    try:
        return _JDateTimeUtils.yearOfCentury(dt, tz.value)
    except Exception as e:
        raise DHError(e) from e
