"""
## Source
https://www.itl.nist.gov/div898/handbook/eda/section3/qqplot.htm

## Purpose
Check If Two Data Sets Can Be Fit With the Same Distribution

The quantile-quantile (q-q) plot is a graphical technique for determining
if two data sets come from populations with a common distribution.

A q-q plot is a plot of the quantiles of the first data set against the
quantiles of the second data set. By a quantile, we mean the fraction
(or percent) of points below the given value. That is, the 0.3 (or 30%)
quantile is the point at which 30% percent of the data fall below and
70% fall above that value.

A 45-degree reference line is also plotted. If the two sets come from a
population with the same distribution, the points should fallapproximately
along this reference line. The greater the departure from this reference
line, the greater the evidence for the conclusion that the two data sets
have come from populations with different distributions.

The advantages of the q-q plot are:
1. The sample sizes do not need to be equal.
2. Many distributional aspects can be simultaneously tested. For example,
shifts in location, shifts in scale, changes in symmetry, and the presence
of outliers can all be detected from this plot. For example, if the two
data sets come from populations whose distributions differ only by a shift
in location, the points should lie along a straight line that is displaced
either up or down from the 45-degree reference line. 

The q-q plot is similar to a probability plot. For a probability plot,
the quantiles for one of the data samples are replaced with the quantiles
of a theoretical distribution.

## Sample Plot
This q-q plot of the JAHANMI2.DAT data set shows that
1. These 2 batches do not appear to have come from populations with a
common distribution.
2. The batch 1 values are significantly higher than the corresponding
batch 2 values.
3. The differences are increasing from values 525 to 625. Then the values
for the 2 batches get closer again. 

## Definition:
Quantiles for Data Set 1 Versus Quantiles of Data Set 2

The q-q plot is formed by:
* Vertical axis: Estimated quantiles from data set 1
* Horizontal axis: Estimated quantiles from data set 2 

Both axes are in units of their respective data sets. That is, the actual
quantile level is not plotted. For a given point on the q-q plot, we know
that the quantile level is the same for both points, but not what that
quantile level actually is.

If the data sets have the same size, the q-q plot is essentially a plot
of sorted data set 1 against sorted data set 2. If the data sets are not
of equal size, the quantiles are usually picked to correspond to the
sorted values from the smaller data set and then the quantiles for the
larger data set are interpolated.

## Questions
The q-q plot is used to answer the following questions:
1. Do two data sets come from populations with a common distribution?
2. Do two data sets have common location and scale?
3. Do two data sets have similar distributional shapes?
4. Do two data sets have similar tail behavior?

## Importance
Check for Common Distribution

When there are two data samples, it is often desirable to know if the
assumption of a common distribution is justified. If so, then location
and scale estimators can pool both data sets to obtain estimates of the
common location and scale. If two samples do differ, it is also useful
to gain some understanding of the differences. The q-q plot can provide
more insight into the nature of the difference than analytical methods
such as the chi-square and Kolmogorov-Smirnov 2-sample tests.

## Related Techniques
* Bihistogram
* T Test
* F Test
* 2-Sample Chi-Square Test
* 2-Sample Kolmogorov-Smirnov Test
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot


def qq_plot(series_1, series_2, x_label="Series 1", y_label="Series 2",
            title="Q-Q Plot", ax=None, show=True, save=False, **kwargs):

    if ax is None:
        fig, ax = plt.subplots()

    # Determining the values to be plotted
    N1, N2 = len(series_1), len(series_2)
    series_1 = sorted(series_1)
    series_2 = sorted(series_2)

    if N1 == N2:
        plotted_series_1 = series_1
        plotted_series_2 = series_2
        
    elif N1 > N2:
        plotted_series_1 = []
        plotted_series_2 = series_2

        for i2 in range(N2):
            i1 = int((N1-1)/(N2-1) * i2)
            plotted_series_1.append(series_1[i1])
            
    else:
        plotted_series_1 = series_1
        plotted_series_2 = []

        for i1 in range(N1):
            i2 = int((N2-1)/(N1-1) * i1)
            plotted_series_2.append(series_2[i2])

    # Scatter plot
    ax.scatter(plotted_series_1, plotted_series_2, **kwargs)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # 45-degree reference line
    min_ = min(series_1[0], series_2[0])
    max_ = max(series_1[-1], series_2[-1])
    ax.plot((min_, max_), (min_, max_))

    show_and_save_plot(show=show, save=save, filename="qq_plot.png")


if __name__ == "__main__":
    df = datasets.load_ceramic_strength()
    batch_1 = df[df["Batch"]==1]["Y"]
    batch_2 = df[df["Batch"]==2]["Y"]
    qq_plot(batch_1, batch_2, x_label="Batch 1", y_label="Batch 2",
            marker="^", alpha=0.7)
