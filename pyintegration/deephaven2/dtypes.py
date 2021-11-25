#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
""" This module defines the data types supported by the Deephaven engine.

Each data type is represented by a DType class which supports creating arrays of the same type and more.
"""
from enum import Enum
from typing import Iterable, Any, List, Tuple

import jpy
import numpy as np
import pandas as pd

from deephaven2 import DHError

_JQstType = jpy.get_type("io.deephaven.qst.type.Type")
_JTableTools = jpy.get_type("io.deephaven.db.tables.utils.TableTools")

# region Deephaven Special Null values for primitive types
# contains appropriate values for bidirectional conversion of null values
NULL_CHAR = 65535  #: Null value for char.
NULL_FLOAT = float.fromhex('-0x1.fffffep127')  #: Null value for float.
NULL_DOUBLE = float.fromhex('-0x1.fffffffffffffP+1023')  #: Null value for double.
NULL_SHORT = -32768  #: Null value for short.
NULL_INT = -0x80000000  #: Null value for int.
NULL_LONG = -0x8000000000000000  #: Null value for long.
NULL_BYTE = -128  #: Null value for byte.


# endregion

def _qst_custom_type(cls_name: str):
    return _JQstType.find(_JTableTools.typeFromName(cls_name))


class DType:
    """ A class represents a data type in Deephaven. """

    def __init__(self, qst_type, j_name):
        self._qst_type = qst_type
        self._j_name = j_name
        self._j_type = jpy.get_type(j_name)

    def __call__(self, *args, **kwargs):
        return self._j_type(*args, **kwargs)

    @property
    def qst_type(self):
        return self._qst_type

    @property
    def j_type(self):
        """ The corresponding Java type. """
        return self._j_type

    def array(self, size: int):
        """ Create a Java array of the same data type of the specified size.

        Args:
            size (int): the size of the array

        Returns:
            a Java array

        Raises:
            DHError
        """
        try:
            return jpy.array(self._j_name, size)
        except Exception as e:
            raise DHError("failed to create a Java array.") from e

    def array_of(self, values: Iterable):
        """ Create a Java array of the same data type populated with values from a Python iterable.

        Args:
            values: a Python iterable of compatible data type

        Returns:
            a Java array

        Raises:
            DHError
        """
        try:
            return jpy.array(self._j_name, values)
        except Exception as e:
            raise DHError("failed to create a Java array.") from e

    def array_from(self, *values):
        ...


class IntegerDType(DType):
    def __init__(self, qst_type, j_name, np_dtypes: Tuple = (), null_value=None):
        self._qst_type = qst_type
        self._j_name = j_name
        self._j_type = jpy.get_type(j_name)
        self.np_types = np_dtypes
        self.null_value = null_value

    def array_from(self, *values):
        try:
            if not values:
                return self.array(0)
            if len(values) == 1 and isinstance(values[0], np.ndarray):
                v = values[0]
                if v.dtype in self.np_types:
                    return self.array_of(v)
                elif np.issubdtype(v.dtype, np.integer):
                    return self.array_of(v.astype(self.np_types[0]))
                elif np.issubdtype(v.dtype, np.floating):
                    np_bool_array = np.isnan(values[0])
                    np_dtype_array = v.astype(self.np_types[0])
                    np_dtype_array[np_bool_array] = self.null_value
                    return self.array_of(np_dtype_array)
                else:
                    raise ValueError(f"Incompatible np dtype ({v.dtype}) for {self.name} array")
            elif len(values) == 1 and isinstance(values[0], pd.Series):
                return self.array_from(values[0].values)
            else:
                return self.array_of(*values)
        except Exception as e:
            raise DHError(e, "failed to create a Java integer array.") from e


class FloatingDType(DType):
    def __init__(self, qst_type, j_name, np_dtypes: Tuple = (), null_value=None):
        self._qst_type = qst_type
        self._j_name = j_name
        self._j_type = jpy.get_type(j_name)
        self.np_types = np_dtypes
        self.null_value = null_value

    def array_from(self, *values):
        """TODO"""


class CharDType(DType):
    def __init__(self, qst_type, j_name, np_dtypes: Tuple = (), null_value=None):
        self._qst_type = qst_type
        self._j_name = j_name
        self._j_type = jpy.get_type(j_name)
        self.np_types = np_dtypes
        self.null_value = null_value

    def array_from(self, *values):
        """TODO"""


# region convenience enum and module level type aliases
class DTypes(Enum):
    bool_ = DType(qst_type=_JQstType.booleanType(), j_name="java.lang.Boolean")
    byte = IntegerDType(qst_type=_JQstType.byteType(), j_name="byte", np_dtypes=(np.int8, np.uint8),
                        null_value=NULL_BYTE)
    int8 = byte
    short = IntegerDType(qst_type=_JQstType.shortType(), j_name="short", np_dtypes=(np.int16, np.uint16),
                         null_value=NULL_SHORT)
    int16 = short
    char = CharDType(qst_type=_JQstType.charType(), j_name="char", null_value=NULL_CHAR)
    int_ = IntegerDType(qst_type=_JQstType.intType(), j_name="int", np_dtypes=(np.int32, np.uint32),
                        null_value=NULL_INT)
    int32 = int_
    long = IntegerDType(qst_type=_JQstType.longType(), j_name="long", np_dtypes=(np.int64, np.uint64),
                        null_value=NULL_LONG)
    int64 = long
    float_ = FloatingDType(qst_type=_JQstType.floatType(), j_name="float", np_dtypes=(np.float32,),
                           null_value=NULL_FLOAT)
    single = float_
    float32 = float_
    double = FloatingDType(qst_type=_JQstType.doubleType(), j_name="double", np_dtypes=(np.float64,),
                           null_value=NULL_DOUBLE)
    float64 = double
    string = DType(qst_type=_JQstType.stringType(), j_name="java.lang.String")
    BigDecimal = DType(qst_type=_qst_custom_type("java.math.BigDecimal"), j_name="java.math.BigDecimal")
    StringSet = DType(qst_type=_qst_custom_type("io.deephaven.db.tables.libs.StringSet"),
                      j_name="io.deephaven.db.tables.libs.StringSet")
    DBDateTime = DType(qst_type=_qst_custom_type("io.deephaven.db.tables.utils.DBDateTime"),
                       j_name="io.deephaven.db.tables.utils.DBDateTime")
    DBPeriod = DType(qst_type=_qst_custom_type("io.deephaven.db.tables.utils.DBPeriod"),
                     j_name="io.deephaven.db.tables.utils.DBPeriod")


bool_ = DTypes.bool_.value
byte = DTypes.byte.value
int8 = DTypes.int8.value
short = DTypes.short.value
int16 = DTypes.int16.value
char = DTypes.char.value
int_ = DTypes.int_.value
int32 = DTypes.int32.value
long = DTypes.long.value
int64 = DTypes.int64.value
float_ = DTypes.float_.value
single = DTypes.single.value
float32 = DTypes.float32.value
double = DTypes.double.value
float64 = DTypes.float64.value
string = DTypes.string.value
BigDecimal = DTypes.BigDecimal.value
StringSet = DTypes.StringSet.value
DBDateTime = DTypes.DBDateTime.value
DBPeriod = DTypes.DBPeriod.value


# endregion

# region helper functions
def j_class_lookup(j_class: Any) -> DType:
    if not j_class:
        return None

    j_type = jpy.get_type(j_class.getName())
    for t in DTypes:
        if t.value.j_type == j_type:
            return t.value

# endregion
