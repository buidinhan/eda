"""
DOE SCATTER PLOT

## Source
https://www.itl.nist.gov/div898/handbook/eda/section3/dexsplot.htm

## Purpose
Determine Important Factors with Respect to Location and Scale

The DOE scatter plot shows the response values for each level of each
factor (i.e., independent) variable. This graphically shows how the
location and scale vary for both within a factor variable and between
different factor variables. This graphically shows which are the
important factors and can help provide a ranked list of important
factors from a designed experiment. The DOE scatter plot is a complement
to the traditional analyis of variance of designed experiments.

DOE scatter plots are typically used in conjunction with the DOE mean
plot and the DOE standard deviation plot. The DOE mean plot replaces the
raw response values with mean response values while the DOE standard
deviation plot replaces the raw response values with the standard
deviation of the response values. There is value in generating all 3 of
these plots. The DOE mean and standard deviation plots are useful in
that the summary measures of location and spread stand out (they can
sometimes get lost with the raw plot). However, the raw data points can
reveal subtleties, such as the presence of outliers, that might get lost
with the summary statistics.

## Sample Plot
Factors 4, 2, 3, and 7 are the Important Factors.

## Description of the Plot
For this sample plot of the BOXBIKE2.DAT data set, there are seven factors
and each factor has two levels. For each factor, we define a distinct
x coordinate for each level of the factor. For example, for factor 1,
level 1 is coded as 0.8 and level 2 is coded as 1.2. The y coordinate is
simply the value of the response variable. The solid horizontal line is
drawn at the overall mean of the response variable. The vertical dotted
lines are added for clarity.

Although the plot can be drawn with an arbitrary number of levels for a
factor, it is really only useful when there are two or three levels for
a factor.

## Conclusions
This sample DOE scatter plot shows that:
1. there does not appear to be any outliers;
2. the levels of factors 2 and 4 show distinct location differences; and
3. the levels of factor 1 show distinct scale differences. 

## Definition
Response Values Versus Factor Variables

DOE scatter plots are formed by:
* Vertical axis: Value of the response variable
* Horizontal axis: Factor variable (with each level of the factor coded
with a slightly offset x coordinate) 

## Questions
The DOE scatter plot can be used to answer the following questions:
1. Which factors are important with respect to location and scale?
2. Are there outliers?

## Importance
Identify Important Factors with Respect to Location and Scale

The goal of many designed experiments is to determine which factors are
important with respect to location and scale. A ranked list of the
important factors is also often of interest. DOE scatter, mean, and
standard deviation plots show this graphically. The DOE scatter plot
additionally shows if outliers may potentially be distorting the results.

DOE scatter plots were designed primarily for analyzing designed
experiments. However, they are useful for any type of multi-factor data
(i.e., a response variable with two or more factor variables having a
small number of distinct levels) whether or not the data were generated
from a designed experiment.

## Extension for Interaction Effects
Using the concept of the scatterplot matrix, the DOE scatter plot can be
extended to display first order interaction effects.

Specifically, if there are k factors, we create a matrix of plots with
k rows and k columns. On the diagonal, the plot is simply a DOE scatter
plot with a single factor. For the off-diagonal plots, we multiply the
values of Xi and Xj. For the common 2-level designs (i.e., each factor
has two levels) the values are typically coded as -1 and 1, so the
multiplied values are also -1 and 1. We then generate a DOE scatter plot
for this interaction variable. This plot is called a DOE interaction
effects plot.

## Related Techniques
* DOE mean plot
* DOE standard deviation plot
* Block plot
* Box plot
* Analysis of variance
"""


from itertools import product

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot


def doe_scatter_plot(df, response, factors, x_labels=None,
                     y_label="Response", title=None,
                     show_overall_mean=False, figure_size=(8, 6),
                     show=True, save=False, **kwargs):

    fig, axes = plt.subplots(nrows=1, ncols=len(factors),
                             sharey=True, figsize=figure_size,
                             gridspec_kw={"left": 0.1, "right": 0.95,
                                          "bottom": 0.1, "top": 0.95,
                                          "wspace": 0,})
    overall_mean = df[response].mean()
    
    for factor, ax in zip(factors, axes):
        if show_overall_mean:
            ax.axhline(y=overall_mean)
        
        factor_levels = np.sort(df[factor].unique())

        def encode(level):
            return factor_levels.searchsorted(level)

        encoded_factors = [encode(x) for x in df[factor]]
        ax.scatter(encoded_factors, df[response], **kwargs)
        ax.set_xticks(list(range(len(factor_levels))))
        ax.set_xticklabels(factor_levels)
        ax.set_xlim(-0.5, len(factor_levels)-0.5)

    if x_labels is None:
        x_labels = factors

    for x_label, ax in zip(x_labels, axes):
        ax.set_xlabel(x_label)
        
    axes[0].set_ylabel(y_label)
    fig.suptitle(title)

    show_and_save_plot(show=show, save=save,
                       filename="doe_scatter_plot.png")
    

def doe_scatter_matrix(df, response, factors, y_label="Response",
                       title=None, figure_size=(8, 6), show=True,
                       save=False, **kwargs):
    
    n_factors = len(factors)

    fig, axes = plt.subplots(nrows=n_factors, ncols=n_factors,
                             squeeze=False, sharey=True,
                             figsize=figure_size,
                             gridspec_kw={"left": 0.1, "right": 0.95,
                                          "bottom": 0.05, "top": 0.9,
                                          "wspace": 0, "hspace": 0.3})

    for pair in product(range(n_factors), range(n_factors)):
        row, col = pair
        ax = axes[row, col]
        
        if row > col: # Skip the cell
            ax.axis("off")
        
        elif row == col: # Single-factor scatter plot
            factor = factors[row]
            factor_levels = np.sort(df[factor].unique())

            def encode(level):
                return factor_levels.searchsorted(level)

            encoded_factors = [encode(x) for x in df[factor]]
            
            ax.scatter(encoded_factors, df[response], **kwargs)
            ax.annotate(factor, xy=(0.5, 1.02), xycoords="axes fraction",
                        horizontalalignment="center")
            
            ax.set_xticks(list(range(len(factor_levels))))
            ax.set_xticklabels(factor_levels)

            ax.set_xlim(-0.5, len(factor_levels)-0.5)

        else: # Double-factor scatter plot
            factor_1 = factors[row]
            factor_2 = factors[col]

            try:
                combined_factor = df[factor_1] * df[factor_2]
                factor_levels = np.sort(combined_factor.unique())

                def encode(level):
                    return factor_levels.searchsorted(level)
                
                encoded_factors = [encode(x) for x in combined_factor]
                
                ax.scatter(encoded_factors, df[response], **kwargs)
                ax.annotate("{}*{}".format(factor_1, factor_2),
                            xy=(0.5, 1.02), xycoords="axes fraction",
                            horizontalalignment="center")
                
                ax.set_xticks(list(range(len(factor_levels))))
                ax.set_xticklabels(factor_levels)

                ax.set_xlim(-0.5, len(factor_levels)-0.5)
                
            except TypeError:
                raise TypeError("Factor levels should be encoded as integers.")
            
    axes[0, 0].set_ylabel(y_label)
    fig.suptitle(title)
    show_and_save_plot(show=show, save=save,
                       filename="doe_scatter_matrix.png")


def test_doe_scatter_plot():
    df = datasets.load_tire_speed_effect()
    doe_scatter_plot(df, "Y", ["X1", "X2", "X3", "X4", "X5"],
                     show_overall_mean=True, figure_size=(6, 6),
                     marker="*", color="g")


def test_doe_scatter_matrix():
    df = datasets.load_tire_speed_effect()
    doe_scatter_matrix(df, "Y", ["X1", "X2", "X3"], marker=".",
                       color="k")


if __name__ == "__main__":
    test_doe_scatter_plot()
    test_doe_scatter_matrix()
