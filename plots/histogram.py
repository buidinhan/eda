"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/histogra.htm

Purpose: Summarize a Univariate Data Set
----------------------------------------
The purpose of a histogram (Chambers) is to graphically summarize the
distribution of a univariate data set. The histogram graphically shows
the following:
1. center (i.e., the location) of the data;
2. spread (i.e., the scale) of the data;
3. skewness of the data;
4. presence of outliers; and
5. presence of multiple modes in the data.

These features provide strong indications of the proper distributional
model for the data. The probability plot or a goodness-of-fit test can
be used to verify the distributional model.

The examples section shows the appearance of a number of common features
revealed by histograms.

Definition
----------
The most common form of the histogram is obtained by splitting the range
of the data into equal-sized bins (called classes). Then for each bin,
the number of points from the data set that fall into each bin are
counted. That is
* Vertical axis: Frequency (i.e., counts for each bin)
* Horizontal axis: Response variable

The classes can either be defined arbitrarily by the user or via some
systematic rule. A number of theoretically derived rules have been
proposed by Scott (Scott 1992).

The cumulative histogram is a variation of the histogram in which the
vertical axis gives not just the counts for a single bin, but rather
gives the counts for that bin plus all bins for smaller values of the
response variable.

Both the histogram and cumulative histogram have an additional variant
whereby the counts are replaced by the normalized counts. The names for
these variants are the relative histogram and the relative cumulative
histogram.

There are two common ways to normalize the counts.
1. The normalized count is the count in a class divided by the total
number of observations. In this case the relative counts are normalized
to sum to one (or 100 if a percentage scale is used). This is the
intuitive case where the height of the histogram bar represents the
proportion of the data in each class.
2. The normalized count is the count in the class divided by the number
of observations times the class width. For this normalization, the area
(or integral) under the histogram is equal to one. From a probabilistic
point of view, this normalization results in a relative histogram that
is most akin to the probability density function and a relative
cumulative histogram that is most akin to the cumulative distribution
function. If you want to overlay a probability density or cumulative
distribution function on top of the histogram, use this normalization.
Although this normalization is less intuitive (relative frequencies
greater than 1 are quite permissible), it is the appropriate
normalization if you are using the histogram to model a probability
density function.

Questions
---------
The histogram can be used to answer the following questions:
1. What kind of population distribution do the data come from?
2. Where are the data located?
3. How spread out are the data?
4. Are the data symmetric or skewed?
5. Are there outliers in the data?

Related Techniques
------------------
* Box plot
* Probability plot
* Frequency Plot
* Stem and Leaf Plot
* Density Trace
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot
from utils.calculations import normal_pdf


def histogram(series, bins=10, x_label="Measure", y_label="Count",
              title=None, edgecolor="k", ax=None, save=False, show=True,
              plot_pdf=False, show_statistics=False, **kwargs):

    # Calculation of Statistics
    mean = np.mean(series)
    std = np.std(series, ddof=1)
    range_ = max(series) - min(series)

    # Histogram
    if ax is None:
        fig, ax = plt.subplots()

    ax.hist(series, bins=bins, edgecolor=edgecolor, **kwargs)

    if show_statistics:
        if x_label is None:
            x_label = ""
            
        x_label += " (mean={:.4f}, std={:.4f}, range={:.4f})".format(
                                                    mean, std, range_)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # PDF Plot
    if plot_pdf:
        Xs = np.arange(mean-3*std, mean+3*std, 6*std/100)
        Ys = normal_pdf(Xs, mean=mean, std=std)
        ax.plot(Xs, Ys)
    
    show_and_save_plot(save=save, show=show, filename="histogram.png")

    return mean, std, range_

if __name__ == "__main__":
    df = datasets.load_heat_flow_meter()
    histogram(df["calibration_factor"], bins=20,
              x_label="Calibration Factor", plot_pdf=True,
              show_statistics=True)
