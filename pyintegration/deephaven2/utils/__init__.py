#
#   Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
import jpy


_JDHConfig = jpy.get_type("io.deephaven.configuration.Configuration")


def get_workspace_root():
    """
    Helper function for extracting the root directory for the workspace configuration
    """
    return _JDHConfig.getInstance().getWorkspacePath()
