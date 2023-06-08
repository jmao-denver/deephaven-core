#
#     Copyright (c) 2016-2023 Deephaven Data Labs and Patent Pending
#
from typing import List

import deephaven.pandas as dhpd
import deephaven.arrow as dhpa
from deephaven import DHError
from deephaven.table import Table

try:
    import riptable as rt
except ImportError:
    raise DHError(message="import riptable failed, please install riptable driver first.")


def to_table(ds: rt.Dataset, cols: List[str] = None) -> Table:
    """Creates a new table from a riptable Dataset.

    Args:
        ds (rt.Dataset): the riptable Dataset instance
        cols (List[str]): the Dataset column names, default is None which means including all columns in the DataFrame

    Returns:
        a Deephaven table

    Raise:
        DHError
    """
    try:
        pa_table = ds.to_arrow()
        return dhpa.to_table(pa_table, cols)
    except:
        pass

    try:
        df = ds.to_pandas()
        return dhpd.to_table(df, cols)
    except DHError:
        raise
    except Exception as e:
        raise DHError(e, message="failed to create a table from a riptable Dataset") from e


def to_dataset(table: Table, cols: List[str] = None) -> rt.Dataset:
    """Creates a riptable Dataset from a table.

    Args:
        table (Table): the source table
        cols (List[str]): the source column names, default is None which means include all columns

    Returns:
        a riptable Dataset

    Raises:
        DHError
    """
    try:
        return rt.Dataset.from_arrow(dhpa.to_arrow(table, cols))
    except:
        pass

    try:
        return rt.Dataset.from_pandas(dhpd.to_pandas(table, cols))
    except DHError:
        raise
    except Exception as e:
        raise DHError(e, "failed to create a riptable Dataset from table.") from e
