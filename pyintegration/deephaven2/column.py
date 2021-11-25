#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import jpy

import deephaven2.dtypes as dtypes
from deephaven2.dtypes import DType

_JColumnHeader = jpy.get_type("io.deephaven.qst.column.header.ColumnHeader")
_JColumn = jpy.get_type("io.deephaven.qst.column.Column")


class ColumnType(Enum):
    NORMAL = 1
    GROUPING = 2
    PARTITIONING = 4
    VIRTUAL = 8

    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class Column:
    """ A Column object represents a column in a Deephaven Table. """
    name: str
    data_type: DType
    component_type: DType = None
    column_type: ColumnType = ColumnType.NORMAL
    input_data: any = field(default=None)

    def j_header(self):
        return _JColumnHeader(self.name, self.data_type.value)

    def j_column(self):
        ...


def byte_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.byte, input_data=values)


def char_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.char, input_data=values)


def short_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.short, input_data=values)


def int_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.int32, input_data=values)


def long_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.long, input_data=values)


def float_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.float, input_data=values)


def double_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.double, input_data=values)


def string_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.string, input_data=values)


def datetime_col(name: str, *values: Any) -> Column:
    return Column(name=name, data_type=dtypes.DBDateTime, input_data=values)


