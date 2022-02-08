#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
""" This module provides various ways to make a Deephaven table. """
from typing import List, Dict, Any

import jpy
from deephaven2.dtypes import DType

from deephaven2 import DHError, dtypes
from deephaven2.column import InputColumn
from deephaven2.table import Table

_JTableFactory = jpy.get_type("io.deephaven.engine.table.TableFactory")
_JTableTools = jpy.get_type("io.deephaven.engine.util.TableTools")
_JDynamicTableWriter = jpy.get_type('io.deephaven.engine.table.impl.util.DynamicTableWriter')
_JReplayer = jpy.get_type('io.deephaven.engine.table.impl.replay.Replayer')


def empty_table(size: int) -> Table:
    """ Creates a table with rows but no columns.

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


def new_table(cols: List[InputColumn]) -> Table:
    """ Creates an in-memory table from a list of input columns. Each column must have an equal number of elements.

    Args:
        cols (List[InputColumn]): a list of InputColumn

    Returns:
        a Table

    Raises:
        DHError
    """
    try:
        return Table(j_table=_JTableFactory.newTable(*[col.j_column for col in cols]))
    except Exception as e:
        raise DHError(e, "failed to create a new time table.") from e


def merge(tables: List[Table]):
    """ Combines two or more tables into one aggregate table. This essentially appends the tables one on top of the
    other. Null tables are ignored.

    Args:
        tables (List[Table]): the source tables

    Returns:
        a Table

    Raises:
        DHError
    """
    try:
        return Table(j_table=_JTableTools.merge([t.j_table for t in tables]))
    except Exception as e:
        raise DHError(e, "merge tables operation failed.") from e


def merge_sorted(tables: List[Table], order_by: str) -> Table:
    """ Combines two or more tables into one sorted, aggregate table. This essentially stacks the tables one on top
    of the other and sorts the result. Null tables are ignored. mergeSorted is more efficient than using merge
    followed by sort.

    Args:
        tables (List[Table]): the source tables
        order_by (str): the name of the key column

    Returns:
         a Table

    Raises:
        DHError
    """
    try:
        return Table(j_table=_JTableTools.mergeSorted(order_by, *[t.j_table for t in tables]))
    except Exception as e:
        raise DHError(e, "merge sorted operation failed.") from e


class DynamicTableWriter:
    """ The DynamicTableWriter creates a new in-memory table and supports writing data to it. This class implements
    the context manager protocol and thus can be used in the with statement.
    """

    def __init__(self, col_defs: Dict[str, DType]):
        """ Initializes the writer and creates a new in-memory table.

        Args:
            col_defs(Dict[str, DTypes]): a map of column names and types of the new table

        Raises:
            DHError
        """
        col_names = list(col_defs.keys())
        col_dtypes = list(col_defs.values())
        try:
            self._j_table_writer = _JDynamicTableWriter(col_names, [t.qst_type for t in col_dtypes])
            self.table = Table(j_table=self._j_table_writer.getTable())
        except Exception as e:
            raise DHError(e, "failed to create a DynamicTableWriter.") from e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """ Closes the writer.

        Raises:
            DHError
        """
        try:
            self._j_table_writer.close()
        except Exception as e:
            raise DHError(e, "failed to close the writer.") from e

    def write_row(self, *values: Any):
        """ Writes a row to the newly created table.

        Args:
            *values (Any): the values of the new row, the data types of these values must match the column definitions
                of the table

        Raises:
             DHError
        """
        try:
            self._j_table_writer.logRow(*values)
        except Exception as e:
            raise DHError(e, "failed to write a row.") from e


class TableReplayer:
    """ The TableReplayer is used to replay historical data with timestamps in a new in-memory table. """

    def __init__(self, start_time: dtypes.DateTime, end_time: dtypes.DateTime):
        """ Initializes the replayer.

        Args:
             start_time (DateTime): historical data start time
             end_time (DateTime): historical data end time

        Raises:
            DHError
        """
        self.start_time = start_time
        self.end_time = end_time
        self._hist_tables = []
        self._replay_tables = []
        try:
            self._j_replayer = _JReplayer(start_time, end_time)
        except Exception as e:
            raise DHError(e, "failed to create a replayer.") from e

    def add_table(self, table: Table, col: str) -> Table:
        """ Adds and prepares a historical data table for replaying.

        Args:
            table (Table): the historical table
            col (str): column in the table containing timestamps

        Returns:
            a new Table

        Raises:
            DHError
        """
        try:
            replay_table = Table(j_table=self._j_replayer.replay(table.j_table, col))
            self._hist_tables.append((table, col))
            self._replay_tables.append(replay_table)
            return replay_table
        except Exception as e:
            raise DHError(e, "failed to add a historical table.") from e

    def start(self):
        """ Starts replaying historical data.

        Raises:
             DHError
        """
        try:
            self._j_replayer.start()
        except Exception as e:
            raise DHError(e, "failed to start the replayer.") from e

    def shutdown(self):
        """ Shuts down and invalidates the replayer. After this call, the replayer can no longer be used. """
        try:
            self._j_replayer.shutdown()
        except Exception as e:
            raise DHError(e, "failed to shutdown the replayer.") from e
