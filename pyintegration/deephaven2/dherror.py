#
#  Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#
import traceback


class DHError(Exception):
    """ A custom exception class for deephaven python integration.
    """

    def __init__(self, cause=None, message=""):
        super().__init__()
        self._message = message
        self._traceback = traceback.format_exc()

        tb_lines = self._traceback.splitlines()
        self._root_cause = ""
        self._compact_tb = []
        for_compact_tb = True
        for tb_ln in tb_lines:
            if tb_ln.startswith("caused by"):
                self._root_cause = tb_ln.split("by")[1].strip()
                if tb_ln.strip().endswith(":"):
                    self._compact_tb.append(tb_ln[:-1].strip())
                else:
                    self._compact_tb.append(tb_ln)
            elif tb_ln.startswith("RuntimeError"):
                self._root_cause = tb_ln
                self._compact_tb.append(tb_ln)
                for_compact_tb = False
            elif tb_ln.startswith("Exception message"):
                self._root_cause = tb_ln.split(":")[1] if ":" in tb_ln else tb_ln
                self._root_cause = self._root_cause.strip()
                self._compact_tb[-1] = self._compact_tb[-1] + f" {self._root_cause}"

            if for_compact_tb:
                self._compact_tb.append(tb_ln)


    @property
    def root_cause(self):
        """ The root cause of the exception. """
        return self._root_cause

    @property
    def traceback(self):
        """ The traceback of the exception. """
        return self._traceback

    @property
    def compact_traceback(self) -> str:
        """ The compact traceback of the exception. """
        return "\n".join(self._compact_tb)

    def __str__(self):
        if self._root_cause:
            return f"{self._message} : {self._root_cause}"
        else:
            return self._message
