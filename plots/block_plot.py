"""
BLOCK PLOT

## Source
https://www.itl.nist.gov/div898/handbook/eda/section3/blockplo.htm

## Purpose
Check to determine if a factor of interest has an effect robust over all
other factors

The block plot (Filliben 1993) is an EDA tool for assessing whether the
factor of interest (the primary factor) has a statistically significant
effect on the response, and whether that conclusion about the primary
factor effect is valid robustly over all other nuisance or secondary
factors in the experiment.

It replaces the analysis of variance test with a less assumption-dependent
binomial test and should be routinely used whenever we are trying to
robustly decide whether a primary factor has an effect.

## Definition
Block Plots are formed as follows:
* Vertical axis: Response variable Y
* Horizontal axis: All combinations of all levels of all nuisance
(secondary) factors X1, X2, ...
* Plot Character: Levels of the primary factor XP

## Advantage
Graphical and binomial

The advantages of the block plot are as follows:
* A quantitative procedure (analysis of variance) is replaced by a
graphical procedure.
* An F-test (analysis of variance) is replaced with a binomial test,
which requires fewer assumptions.

## Questions
The block plot can provide answers to the following questions:
1. Is the factor of interest significant?
2. Does the factor of interest have an effect?
3. Does the location change between levels of the primary factor?
4. Has the process improved?
5. What is the best setting (= level) of the primary factor?
6. How much of an average improvement can we expect with this best
setting of the primary factor?
7. Is there an interaction between the primary factor and one or more
nuisance factors?
8. Does the effect of the primary factor change depending on the setting
of some nuisance factor?
9. Are there any outliers?

## Importance
Robustly checks the significance of the factor of interest

The block plot is a graphical technique that pointedly focuses on whether
or not the primary factor conclusions are in fact robustly general. This
question is fundamentally different from the generic multi-factor
experiment question where the analyst asks, "What factors are important
and what factors are not" (a screening problem)? Global data analysis
techniques, such as analysis of variance, can potentially be improved by
local, focused data analysis techniques that take advantage of this
difference.
"""


import itertools

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot


def block_plot(df, response_name, plot_factor, grouping_factors,
               x_label=None, y_label=None, plot_factor_label=None,
               title=None, ax=None, figure_size=(6, 6), show=True,
               save=False):

    # Levels of the plot factor
    plot_levels = np.sort(df[plot_factor].unique())

    # Combinations of the grouping factors
    levels_by_factor = {}
    for factor in grouping_factors:
        levels_by_factor[factor] = np.sort(df[factor].unique())

    # Combinations = Levels_of_Factor_1 x Levels_of_Factor_2 x ...
    # (Cartesian product)
    combinations = list(itertools.product(*(levels_by_factor.values())))

    # Calculating response means grouped by all factors
    groups = df[[response_name,
                 plot_factor,
                 *grouping_factors]].groupby([*grouping_factors,
                                              plot_factor])
    grouped_response_means = groups.mean()

    # Response means grouped by grouping factors
    response_means_by_combination = {}
    for combination in combinations:
        response_means_by_combination[combination] = {}
        try:
            for plot_level in plot_levels:
                response_means_by_combination[combination][plot_level] = \
                    grouped_response_means.loc[(*combination, plot_level),
                                               response_name]
        except KeyError:
            continue

    # Plotting
    if ax is None:
        fig, ax = plt.subplots(gridspec_kw={"bottom": 0.15, "top": 0.95,
                                            "left": 0.1, "right": 0.96},
                               figsize=figure_size)

    for index, combination in enumerate(combinations):
        response_means_for_this_combination = \
                            response_means_by_combination[combination]
                                            
        if len(response_means_for_this_combination) <= 1:
            continue
        
        low = min(response_means_for_this_combination.values())
        high = max(response_means_for_this_combination.values())
        ax.bar(index, high-low, width=0.5, bottom=low, align="center",
               edgecolor="k", color="w")
        
        for plot_level in response_means_for_this_combination.keys():
            mean_at_this_level = \
                response_means_for_this_combination[plot_level]

            if mean_at_this_level not in (low, high):
                ax.plot([index], [mean_at_this_level], marker="^",
                        color="k")

            ax.annotate(str(plot_level),
                        xy=(index, mean_at_this_level),
                        xycoords="data",
                        xytext=(-2, 1),
                        textcoords="offset points")

    if plot_factor_label is not None:
        plot_factor_label = "Plot Character = " + plot_factor_label
        ax.annotate(plot_factor_label,
                    xy=(0.01, 0.97),
                    xycoords="axes fraction")

    x_ticks = [index for index in range(len(combinations))]
    ax.set_xticks(x_ticks)

    if len(grouping_factors) > 1:
        x_tick_labels = [str(combination) for combination in
                         combinations]
        ax.set_xticklabels(x_tick_labels, rotation=60)
    else:
        x_tick_labels = [str(combination[0]) for combination in
                         combinations]
        ax.set_xticklabels(x_tick_labels)
        
    if x_label is None:
        if len(grouping_factors) > 1:
            x_label = "(" + ", ".join(grouping_factors) + ")"
        else:
            x_label = grouping_factors[0]

    if y_label is None:
        y_label = "Average Response"

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    show_and_save_plot(show=show, save=save, filename="block_plot.png")
            

def test_1():
    df = datasets.load_lead_wire_weld()    
    block_plot(df, "Defects", "Weld", ["Plant", "Speed", "Shift"],
               title="Block Plot", x_label="Plant(2) x Speed(2) x Shift(3)",
               y_label="Average Detects per Hour",
               plot_factor_label="Weld Method(2)")


def test_2():
    df = datasets.load_ceramic_strength()
    block_plot(df, "Y", "Batch", ["Lab", "X1"])


if __name__ == "__main__":
    test_1()
    test_2()
