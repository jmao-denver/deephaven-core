//
// Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
//
package io.deephaven.plot.example_plots;

import io.deephaven.plot.Figure;
import io.deephaven.plot.FigureFactory;


public class SimpleXYHisto {

    public static void main(String[] args) {
        final Number[] x1 = {1, 2, 2, 3, 3, 3, 4};

        Figure fig = FigureFactory.figure();
        Figure cht = fig.newChart(0)
                .chartTitle("Chart Title");
        Figure axs = cht.newAxes()
                .xLabel("X")
                .yLabel("Y")
                .histPlot("Test1", x1, 4).pointColor("green");

        ExamplePlotUtils.display(axs);
    }

}
