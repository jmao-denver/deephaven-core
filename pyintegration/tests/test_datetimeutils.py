#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#

import unittest
from time import sleep

from deephaven2.constants import NULL_LONG
from deephaven2.datetimeutils import *


class DateTimeUtilsTestCase(unittest.TestCase):
    def test_convert_datetime(self):
        datetime_str = "2021-12-10T23:59:59"
        timezone_str = "NY"
        dt = convert_datetime(f"{datetime_str} {timezone_str}")
        print(dt)
        self.assertTrue(str(dt).startswith(datetime_str))

        with self.assertRaises(DHError) as cm:
            datetime_str = "2021-12-10T23:59:59"
            timezone_str = "--"
            dt = convert_datetime(f"{datetime_str} {timezone_str}")
        self.assertIn("RuntimeException", str(cm.exception))

    def test_convert_period(self):
        period_str = "1W"
        period = convert_period(period_str)
        self.assertEqual(str(period).upper(), period_str)

        period_str = "T1M"
        period = convert_period(period_str)
        self.assertEqual(repr(period).upper(), period_str)

        with self.assertRaises(DHError) as cm:
            period_str = "T1Y"
            period = convert_period(period_str)
        self.assertIn("RuntimeException", str(cm.exception))

    def test_convert_time(self):
        time_str = "530000:59:39.123456789"
        in_nanos = convert_time(time_str)
        self.assertEqual(str(in_nanos), "1908003579123456789")

        with self.assertRaises(DHError) as cm:
            time_str = "530000:59:39.X"
            in_nanos = convert_time(time_str)
        self.assertIn("RuntimeException", str(cm.exception))

        time_str = "00:59:39.X"
        in_nanos = convert_time(time_str, quiet=True)
        self.assertEqual(in_nanos, NULL_LONG)

    def test_current_time_and_diff(self):
        dt = current_time()
        sleep(1)
        dt1 = current_time()
        self.assertGreaterEqual(diff_nanos(dt, dt1), 100000000)

    def test_date_at_midnight(self):
        dt = current_time()
        mid_night_time_ny = date_at_midnight(dt, TimeZone.NY)
        mid_night_time_pt = date_at_midnight(dt, TimeZone.PT)
        self.assertGreaterEqual(diff_nanos(mid_night_time_ny, mid_night_time_pt), 0)

    def test_day_of_month(self):
        ...


if __name__ == '__main__':
    unittest.main()
