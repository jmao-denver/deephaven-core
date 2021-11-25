#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#

import unittest

import jpy
import numpy
import numpy as np
import pandas as pd

from deephaven2 import dtypes
from deephaven2.dtypes import DTypes
from tests.testbase import BaseTestCase


class DTypesTestCase(BaseTestCase):
    def test_type_alias(self):
        self.assertEqual(DTypes.short, DTypes.int16)

    def test_jdb_type(self):
        self.assertEqual(dtypes.short.j_type, jpy.get_type("short"))

    def test_qst_type(self):
        self.assertIn(".qst.type.", str(dtypes.short.qst_type))

    def test_custom_type(self):
        self.assertIn("CustomType", str(dtypes.StringSet.qst_type))

    def test_period(self):
        hour_period = dtypes.DBPeriod.j_type("T1H")
        self.assertTrue(isinstance(hour_period, dtypes.DBPeriod.j_type))

    def test_callable(self):
        big_decimal = dtypes.BigDecimal(12.88)
        self.assertIn("12.88", str(big_decimal))

        big_decimal1 = dtypes.BigDecimal("12.88")
        self.assertTrue(big_decimal.compareTo(big_decimal1))

    def test_array(self):
        j_array = dtypes.int_.array(5)
        for i in range(5):
            j_array[i] = i
        np_array = numpy.frombuffer(j_array, numpy.int32)
        self.assertTrue((np_array == numpy.array([0, 1, 2, 3, 4], dtype=numpy.int32)).all())

    def test_array_of(self):
        j_array = dtypes.int_.array_of(range(5))
        np_array = numpy.frombuffer(j_array, numpy.int32)
        self.assertTrue((np_array == numpy.array([0, 1, 2, 3, 4], dtype=numpy.int32)).all())

    def test_integer_array_from(self):
        np_array = np.array([np.log(-1.), 1., np.log(0)])
        j_array = dtypes.int64.array_from(np_array)
        self.assertIsNotNone(j_array)

        j_array = dtypes.int64.array_from(np_array)
        for x in j_array:
            print(x)
        self.assertIsNotNone(j_array)

        j_array = dtypes.short.array_from(np_array)
        for x in j_array:
            print(x)
        self.assertIsNotNone(j_array)

        pd_series = pd.Series(np_array)
        j_array = dtypes.int64.array_from(pd_series)
        self.assertIsNotNone(j_array)

        j_array = dtypes.int64.array_from()
        self.assertIsNotNone(j_array)

        j_array = dtypes.int64.array_from([1.1, 2.2, 3.3])
        self.assertIsNotNone(j_array)


if __name__ == '__main__':
    unittest.main()
