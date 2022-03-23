#
#   Copyright (c) 2016-2022 Deephaven Data Labs and Patent Pending
#
from enum import Enum

import jpy

from deephaven2._wrapper_abc import JObjectWrapper
from .linestyle import LineStyle
from .color import Color
from .font import Font, FontStyle

_JAxisTransform = jpy.get_type("io.deephaven.plot.axistransformations.AxisTransform")
_JShapes = jpy.get_type("io.deephaven.gui.shape.JShapes")
_JPlotStyle = jpy.get_type("io.deephaven.plot.PlotStyle")
_JAxisFormat = jpy.get_type("io.deephaven.plot.axisformatters.AxisFormat")


class PlotStyle(Enum):
    """ An enum defining the styles of a plot (e.g. line, bar, etc.). """

    BAR = _JPlotStyle.BAR
    """ A bar chart. """

    STACKED_BAR = _JPlotStyle.STACKED_BAR
    """ A stacked bar chart. """

    LINE = _JPlotStyle.LINE
    """ A line chart (does not display shapes at data points by default). """

    AREA = _JPlotStyle.AREA
    """ An area chart (does not display shapes at data points by default). """

    STACKED_AREA = _JPlotStyle.STACKED_AREA
    """ A stacked area chart (does not display shapes at data points by default). """

    PIE = _JPlotStyle.PIE
    """ A pie chart. """

    HISTOGRAM = _JPlotStyle.HISTOGRAM
    """ A histogram chart. """

    OHLC = _JPlotStyle.OHLC
    """ An open-high-low-close chart. """

    SCATTER = _JPlotStyle.SCATTER
    STEP = _JPlotStyle.STEP
    """ A scatter plot (lines are not displayed by default). """

    ERROR_BAR = _JPlotStyle.ERROR_BAR
    """ An error bar plot (points are not displayed by default). """


class AxisFormat:
    ...


class BusinessCalendar:
    ...


class Shape:
    ...


class AxisTransform:
    ...


class SelectableDataSet(JObjectWrapper):
    def __init__(self, j_sds):
        self.j_sds = j_sds

    @property
    def j_object(self) -> jpy.JType:
        return self.j_sds
