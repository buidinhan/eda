"""
DOE MEAN PLOT

## Source
https://www.itl.nist.gov/div898/handbook/eda/section3/dexmeanp.htm
https://www.itl.nist.gov/div898/handbook/eda/section3/dexsdplo.htm

## Purpose
Detect Important Factors With Respect to Location
The DOE mean plot is appropriate for analyzing data from a designed
experiment, with respect to important factors, where the factors are at
two or more levels. The plot shows mean values for the two or more
levels of each factor plotted by factor. The means for a single factor
are connected by a straight line. The DOE mean plot is a complement to
the traditional analysis of variance of designed experiments.

This plot is typically generated for the mean. However, it can be
generated for other location statistics such as the median.

## Definition
Mean Response Versus Factor Variables

DOE mean plots are formed by:
* Vertical axis: Mean of the response variable for each level of the
factor
* Horizontal axis: Factor variable

## Questions
The DOE mean plot can be used to answer the following questions:
1. Which factors are important? The DOE mean plot does not provide a
definitive answer to this question, but it does help categorize factors
as "clearly important", "clearly not important", and "borderline
importance".
2. What is the ranking list of the important factors?

## Importance
Determine Significant Factors

The goal of many designed experiments is to determine which factors are
significant. A ranked order listing of the important factors is also
often of interest. The DOE mean plot is ideally suited for answering
these types of questions and we recommend its routine use in analyzing
designed experiments.

## Extension for Interaction Effects
Using the concept of the scatter plot matrix, the DOE mean plot can be
extended to display first-order interaction effects.

Specifically, if there are k factors, we create a matrix of plots with
k rows and k columns. On the diagonal, the plot is simply a DOE mean
plot with a single factor. For the off-diagonal plots, measurements at
each level of the interaction are plotted versus level, where level is
Xi times Xj and Xi is the code for the ith main effect level and Xj is
the code for the jth main effect. For the common 2-level designs (i.e.,
each factor has two levels) the values are typically coded as -1 and 1,
so the multiplied values are also -1 and 1. We then generate a DOE mean
plot for this interaction variable. 
"""


from itertools import product

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot


def doe_statistic_plot(df, response, factors, statistic="mean",
                       x_labels=None, y_label=None, title=None,
                       show_overall_statistic=False, figure_size=(8, 6),
                       show=True, save=False, **kwargs):

    fig, axes = plt.subplots(nrows=1, ncols=len(factors),
                             sharey=True, figsize=figure_size,
                             gridspec_kw={"left": 0.1, "right": 0.95,
                                          "bottom": 0.1, "top": 0.95,
                                          "wspace": 0,})
    if statistic == "mean":
        overall_statistic = df[response].mean()
    elif statistic == "median":
        overall_statistic = df[response].median()
    elif statistic == "std":
        overall_statistic = df[response].std()
    else:
        raise ValueError("*statistic* should be 'mean', 'median', or 'std'.")    
    
    for factor, ax in zip(factors, axes):
        if show_overall_statistic:
            ax.axhline(y=overall_statistic)
        
        factor_levels = np.sort(df[factor].unique())

        # levels -> 0, 1, 2, ...
        def encode(level):
            return factor_levels.searchsorted(level)

        encoded_levels = [encode(x) for x in factor_levels]

        stat_by_level = []
        for level in factor_levels:
            if statistic == "mean":
                stat_by_level.append(
                    df[df[factor]==level][response].mean())
            elif statistic == "median":
                stat_by_level.append(
                    df[df[factor]==level][response].median())
            elif statistic == "std":
                stat_by_level.append(
                    df[df[factor]==level][response].std())
            else:
                raise ValueError(
                    "*statistic* should be 'mean', 'median', or 'std'.")
                                     
        ax.plot(encoded_levels, stat_by_level, **kwargs)
        ax.set_xticks(list(range(len(factor_levels))))
        ax.set_xticklabels(factor_levels)
        ax.set_xlim(-0.5, len(factor_levels)-0.5)

    if x_labels is None:
        x_labels = factors

    for x_label, ax in zip(x_labels, axes):
        ax.set_xlabel(x_label)

    if y_label is None:
        y_label = statistic.title() + " of Response"
        
    axes[0].set_ylabel(y_label)
    fig.suptitle(title)

    show_and_save_plot(show=show, save=save,
                       filename="doe_scatter_plot.png")


def doe_statistic_matrix():
    pass


def test_doe_statistic_plot():
    df = datasets.load_tire_speed_effect()
    doe_statistic_plot(df, "Y", ["X1", "X2", "X3", "X4", "X5", "X6", "X7"],
                       statistic="mean", show_overall_statistic=True,
                       title="DOE Mean Plot", y_label="Sensitivity",
                       marker="o")


def test_doe_statistic_matrix():
    pass


if __name__ == "__main__":
    test_doe_statistic_plot()
    test_doe_statistic_matrix()
