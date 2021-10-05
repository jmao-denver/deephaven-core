#
#  Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
"""Demo how to run a Python script on the server and open a table generated by the script."""
import pandas as pd

from examples.import_test_data import import_taxi_records
from pydeephaven import Session, Table


def run_script(dh_session: Session) -> Table:
    server_script = '''
t2 = t.where("VendorID > 0")\
        .sort("VendorID", "fare_amount")\
        .headBy(5, "VendorID")
'''
    dh_session.run_script(server_script)
    return dh_session.open_table("t2")


def main():
    with Session(host="localhost", port=10000) as dh_session:
        taxi_data_table = import_taxi_records(dh_session)
        variable_name = "t"
        dh_session.bind_table(variable_name, taxi_data_table)

        bottom_5_fares_table = run_script(dh_session=dh_session)
        snapshot_data = bottom_5_fares_table.snapshot()
        df = snapshot_data.to_pandas()

        pd.set_option("max_columns", 20)
        print(df)


if __name__ == '__main__':
    main()
