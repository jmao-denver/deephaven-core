#
# Copyright (c) 2016-2022 Deephaven Data Labs and Patent Pending
#
import string
import unittest
from typing import Any, List, Optional, Union

import numpy as np
import riptable as rt
from riptable import (
    Dataset,
)
from riptable.rt_enum import (
    CategoryMode,
    TypeRegister,
)

import deephaven.pandas as dhpd
import deephaven.riptable as dhrt
from deephaven import new_table, dtypes
from deephaven.column import byte_col, char_col, short_col, bool_col, int_col, long_col, float_col, double_col, \
    string_col, datetime_col
from deephaven.constants import NULL_LONG
from tests.testbase import BaseTestCase

_N = 10


def get_categorical_base_data() -> List[List[str]]:
    # This acts a a base for the different edge cases considered for the type of data that is used when constructing
    # a Categorical. The other Categorical data functions, such as the one for bytes and numerics, derive from this table.
    # If new edge cases are considered, this table can be extended which will extend tables for the other data types.
    return [
        # [],  # empty list; commented out since this case throws a ValueError in Categorical constructor.
        ["a"],  # one element list
        ["a"] * _N,  # list of single repeated element
        list(string.ascii_letters),  # list of all unique elements
        ["a"] * _N + ["z"] + ["a"] * _N,  # repeats surrounding single unique
        ["a"] + ["b"] * _N + ["c"],  # single unique surrounded by repeats
    ]


def _get_categorical_byte_data() -> List[List[bytes]]:
    bytes = []
    for values in get_categorical_base_data():
        b = [s.encode("utf-8") for s in values]
        bytes.extend(b)
    return bytes


def _get_categorical_numeric_data() -> List[List[int]]:
    numerics = []
    for values in get_categorical_base_data():
        numerics.append([ord(c) for c in values])
    return numerics


def _get_categorical_multikey_data() -> List[List[rt.FastArray]]:
    # Create data that can be used to construct MultiKey Categoricals where both keys are
    # strings, numerics, and combination of the two.
    strings = get_categorical_base_data()
    numerics = _get_categorical_numeric_data()

    results = []
    # consider parameterizing over the number of keys instead of literal handling of up to four keys
    for values in strings + numerics:  # two keys of same dtype and value
        results.append([rt.FA(values), rt.FA(values)])
    for values, values1 in zip(strings, numerics):  # two keys of different dtypes
        results.append([rt.FA(values), rt.FA(values1)])
    for values, values1, values2 in zip(strings, strings, numerics):  # three keys of different dtypes
        results.append([rt.FA(values), rt.FA(values1), rt.FA(values2)])
    for values, values1, values2, values3 in zip(strings, strings, strings, numerics):  # four keys of different dtypes
        results.append([rt.FA(values), rt.FA(values1), rt.FA(values2), rt.FA(values3)])
    return results


def get_categorical_data_factory_method(
        category_modes: Optional[Union[CategoryMode, List[CategoryMode]]] = None
) -> List[List[Any]]:
    if category_modes is None:  # return all types of categories
        return get_categorical_base_data() + _get_categorical_numeric_data() #+ _get_categorical_multikey_data()
    if not isinstance(category_modes, list):  # wrap single category mode in a list
        category_modes = [category_modes]

    underlying_data = []
    if rt.rt_enum.CategoryMode.StringArray in category_modes:
        underlying_data.extend(get_categorical_base_data())
    if rt.rt_enum.CategoryMode.NumericArray in category_modes:
        underlying_data.extend(_get_categorical_numeric_data())
    if rt.rt_enum.CategoryMode.MultiKey in category_modes:
        underlying_data.extend(_get_categorical_multikey_data())
    return underlying_data


def get_all_categorical_data() -> List[rt.Categorical]:
    """Returns a list of all the Categorical test data of all supported CategoryModes."""
    return [rt.Categorical(data) for data in get_categorical_data_factory_method()]


class RiptableTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        input_cols = [
            bool_col(name="Boolean", data=[True, False]),
            byte_col(name="Byte", data=(1, -1)),
            char_col(name="Char", data='-1'),
            short_col(name="Short", data=[1, -1]),
            int_col(name="Int", data=[1, -1]),
            long_col(name="Long", data=[1, -1]),
            long_col(name="NPLong", data=np.array([1, -1], dtype=np.int8)),
            float_col(name="Float", data=[1.01, -1.01]),
            double_col(name="Double", data=[1.01, -1.01]),
            string_col(name="String", data=["foo", "bar"]),
            datetime_col(name="Datetime", data=[dtypes.DateTime(1), dtypes.DateTime(-1)]),
        ]
        self.test_table = new_table(cols=input_cols)

    def tearDown(self) -> None:
        self.test_table = None
        super().tearDown()

    def test_to_riptable(self):
        ds = dhrt.to_dataset(self.test_table)
        self.assertEqual(len(ds), self.test_table.size)
        t = dhrt.to_table(ds)
        self.assert_table_equals(t, self.test_table)

    def test_to_table_categorical(self):
        for categorical in get_all_categorical_data():
            with self.subTest(categorical):
                k = "categorical"
                ds = Dataset({k: categorical})
                df = ds.to_pandas()
                t = dhrt.to_table(ds)
                df_t = dhpd.to_pandas(t, dtype_backend="numpy_nullable")
                ds1 = Dataset.from_pandas(df_t)
                self.assertEqual(len(df), len(df_t))
                self.assertTrue(ds.equals(ds1))
                # DH doesn't support Multikey Categorical data
                self.assertNotEqual(ds.dtypes, ds1.dtypes)

        for categorical in [rt.Categorical(data) for data in _get_categorical_multikey_data()]:
            with self.subTest(categorical):
                k = "categorical_mk"
                ds = Dataset({k: categorical})
                df = ds.to_pandas()
                t = dhrt.to_table(ds)
                df_t = dhpd.to_pandas(t, dtype_backend="numpy_nullable")
                ds1 = Dataset.from_pandas(df_t)
                self.assertEqual(len(df), len(df_t))
                # DH doesn't support Categorical data
                self.assertNotEqual(ds.dtypes, ds1.dtypes)
                self.assertFalse(ds.equals(ds1))

    def test_to_table_datetime(self):
        dtn = TypeRegister.DateTimeNano([1541239200000000000, 1541325600000000000], from_tz="NYC", to_tz="NYC")
        dts = dtn.hour_span
        ds = Dataset({"dtn": dtn, "dts": dts})
        t = dhrt.to_table(ds)
        self.assertTrue(ds.equals(dhrt.to_dataset(t)))


if __name__ == '__main__':
    unittest.main()
