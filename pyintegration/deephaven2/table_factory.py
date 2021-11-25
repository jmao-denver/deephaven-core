#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
""" This module provides various ways to make a Deephaven table. """
from typing import List

import jpy

from deephaven2.column import Column
from deephaven2 import DHError
from deephaven2.table import Table, _JTableTools

# _JTableFactory = jpy.get_type("io.deephaven.engine.table.TableFactory")
_JTableTools = jpy.get_type("io.deephaven.db.tables.utils.TableTools")


def empty_table(size: int) -> Table:
    """ Create an empty table.

    Args:
        size (int): the number of rows

    Returns:
         a Table

    Raises:
        DHError
    """
    try:
        return Table(j_table=_JTableTools.emptyTable(size))
    except Exception as e:
        raise DHError(e, "failed to create an empty table.") from e


def time_table(period: str, start_time: str = None) -> Table:
    """ Creates a table that adds a new row on a regular interval.

    Args:
        period (str): time interval between new row additions
        start_time (str): start time for adding new rows

    Returns:
        a Table

    Raises:
        DHError
    """
    try:
        if start_time:
            return Table(j_table=_JTableTools.timeTable(start_time, period))
        else:
            return Table(j_table=_JTableTools.timeTable(period))

    except Exception as e:
        raise DHError(e, "failed to create a time table.") from e


def new_table(cols: List[Column]) -> Table:
    """ Creates an in-memory table from a list of columns. Each column must have an equal number of elements.
    """
    return _JTableFactory.newTable(*[col.j_column for col in cols])


def merge(*args):
    """
    Concatenates multiple Deephaven Tables into a single Table.


     The resultant table will have rows from the same table together, in the order they are specified as inputs.


     When ticking tables grow, they may run out of the 'pre-allocated' space for newly added rows. When more key-
     space is needed, tables in higher key-space are shifted to yet higher key-space to make room for new rows. Shifts
     are handled efficiently, but some downstream operations generate a linear O(n) amount of work per shifted row.
     When possible, one should favor ordering the constituent tables first by static/non-ticking sources followed by
     tables that are expected to grow at slower rates, and finally by tables that grow without bound.

    *Overload 1*
      :param theList: (java.util.List<io.deephaven.db.tables.Table>) - a List of Tables to be concatenated
      :return: (io.deephaven.db.tables.Table) a Deephaven table object

    *Overload 2*
      :param tables: (java.util.Collection<io.deephaven.db.tables.Table>) - a Collection of Tables to be concatenated
      :return: (io.deephaven.db.tables.Table) a Deephaven table object

    *Overload 3*
      :param tables: (io.deephaven.db.tables.Table...) - a list of Tables to be concatenated
      :return: (io.deephaven.db.tables.Table) a Deephaven table object
    """

    return _JTableTools.merge(*args)


def merge_sorted(keyColumn, *tables):
    """
    Concatenates multiple sorted Deephaven Tables into a single Table sorted by the specified key column.

     The input tables must each individually be sorted by keyColumn, otherwise results are undefined.

    *Overload 1*
      :param keyColumn: (java.lang.String) - the column to use when sorting the concatenated results
      :param tables: (io.deephaven.db.tables.Table...) - sorted Tables to be concatenated
      :return: (io.deephaven.db.tables.Table) a Deephaven table object

    *Overload 2*
      :param keyColumn: (java.lang.String) - the column to use when sorting the concatenated results
      :param tables: (java.util.Collection<io.deephaven.db.tables.Table>) - a Collection of sorted Tables to be concatenated
      :return: (io.deephaven.db.tables.Table) a Deephaven table object
    """

    return _JTableTools.mergeSorted(keyColumn, *tables)
