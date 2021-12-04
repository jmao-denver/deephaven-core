#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
import time
import unittest
from dataclasses import dataclass

import jpy

from deephaven2 import DHError, dtypes
from deephaven2.column import byte_col, char_col, short_col, bool_col, int_col, long_col, float_col, double_col, \
    string_col, datetime_col, jobj_col
from tests.testbase import BaseTestCase

JArrayList = jpy.get_type("java.util.ArrayList")


class ColumnTestCase(BaseTestCase):

    def test_column_error(self):
        jobj = JArrayList()
        jobj.add(1)
        jobj.add(-1)
        with self.assertRaises(DHError) as cm:
            _ = bool_col(name="Boolean", data=[True, 'abc']).j_column

        with self.assertRaises(DHError) as cm:
            _ = byte_col(name="Byte", data=[1, 'abc']).j_column

        with self.assertRaises(DHError) as cm:
            _ = char_col(name="Char", data=[jobj]).j_column

        with self.assertRaises(DHError) as cm:
            _ = short_col(name="Short", data=[1, 'abc']).j_column

        with self.assertRaises(DHError) as cm:
            _ = int_col(name="Int", data=[1, [1, 2]]).j_column

        with self.assertRaises(DHError) as cm:
            _ = long_col(name="Long", data=[1, float('inf')]).j_column

        with self.assertRaises(DHError) as cm:
            _ = float_col(name="Float", data=[1.01, 'NaN']).j_column

        with self.assertRaises(DHError) as cm:
            _ = double_col(name="Double", data=[1.01, jobj]).j_column

        with self.assertRaises(DHError) as cm:
            _ = string_col(name="String", data=[1, -1.01]).j_column

        with self.assertRaises(DHError) as cm:
            _ = datetime_col(name="Datetime", data=[dtypes.DateTime(round(time.time())), False]).j_column

        with self.assertRaises(DHError) as cm:
            _ = jobj_col(name="JObj", data=[jobj, CustomClass(-1, "-1")]).j_column


@dataclass
class CustomClass:
    f1: int
    f2: str


if __name__ == '__main__':
    unittest.main()
