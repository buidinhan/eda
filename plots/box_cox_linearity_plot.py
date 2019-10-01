"""
BOX-COX LINEARITY PLOT

## Source
https://www.itl.nist.gov/div898/handbook/eda/section3/boxcoxli.htm

## Purpose
Find the transformation of the X variable that maximizes the correlation
between a Y and an X variable

When performing a linear fit of Y against X, an appropriate transformation
of X can often significantly improve the fit. The Box-Cox transformation
(Box and Cox, 1964) is a particularly useful family of transformations.
It is defined as: T(X) = (X^λ − 1) / λ, where X is the variable being
transformed and λ is the transformation parameter. For λ = 0, the natural
log of the data is taken instead of using the above formula.

The Box-Cox linearity plot is a plot of the correlation between Y and the
transformed X for given values of λ. That is, λ is the coordinate for the
horizontal axis variable and the value of the correlation between Y and
the transformed X is the coordinate for the vertical axis of the plot.
The value of λ corresponding to the maximum correlation (or minimum for
negative correlation) on the plot is then the optimal choice for λ.

Transforming X is used to improve the fit. The Box-Cox transformation
applied to Y can be used as the basis for meeting the error assumptions.
That case is not covered here. See page 225 of (Draper and Smith, 1981)
or page 77 of (Ryan, 1997) for a discussion of this case.

## Definition
Box-Cox linearity plots are formed by
* Vertical axis: Correlation coefficient from the transformed X and Y
* Horizontal axis: Value for λ 

## Questions
The Box-Cox linearity plot can provide answers to the following questions:
1. Would a suitable transformation improve my fit?
2. What is the optimal value of the transformation parameter?

## Importance
Find a suitable transformation

Transformations can often significantly improve a fit. The Box-Cox
linearity plot provides a convenient way to find a suitable
transformation without engaging in a lot of trial and error fitting.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from utils import datasets
from utils.calculations import box_cox_transformation
from utils.plotting import show_and_save_plot
from plots import scatter_plot


def box_cox_linearity_plot(X, Y, lambda_min=-2, lambda_max=2, N=100,
                           title=None, ax=None, show=True, save=False):

    # Calculating lambda values and corresponding correlation coefficients
    lambdas = np.linspace(lambda_min, lambda_max, N)
    Rs = []
    for lambda_ in lambdas:
        transformed_X = box_cox_transformation(X, lambda_)
        _, _, R, _, _ = stats.linregress(transformed_X, Y)
        Rs.append(R)

    Rs = np.array(Rs)
    Rs_squared = Rs ** 2

    optimal_index = Rs_squared.argmax()
    optimal_lambda = lambdas[optimal_index]
    optimal_R = Rs[optimal_index]
        
    # Plotting
    if ax is None:
        fig, ax = plt.subplots(gridspec_kw={"bottom": 0.2},
                               figsize=(6, 4))

    ax.scatter(lambdas, Rs, marker="x")
    ax.set_title(title)
    ax.set_ylabel("Correlation Coefficient")

    x_label = "λ\n"
    x_label += "Best R={:.3f} at λ={:.3f}".format(optimal_R, optimal_lambda)
    ax.set_xlabel(x_label)
               
    show_and_save_plot(show=show, save=save,
                       filename="box_cox_linearity.png")

    return lambdas, Rs, optimal_lambda, optimal_R


def box_cox_linearity_set(X, Y, main_title=None, show=True, save=False,
                          box_cox_kws=None, original_lin_kws=None,
                          transformed_lin_kws=None):

    fig, axes = plt.subplots(nrows=2, ncols=2,
                             gridspec_kw={
                                 "left": 0.1, "right": 0.98,
                                 "bottom": 0.15, "top": 0.9,
                                 "wspace": 0.3, "hspace": 0.6,
                                 },
                             figsize=(7, 8))
    org_lin, box_cox = axes[0]
    trans_lin, _ = axes[1]

    fig.suptitle(main_title)

    # Box-Cox Linearity Plot
    if box_cox_kws is None:
        box_cox_kws = {"title": "Box-Cox Transformation"}

    lambdas, Rs, optimal_lambda, optimal_R = \
             box_cox_linearity_plot(X, Y, ax=box_cox, show=False,
                                    save=False, **box_cox_kws)

    x_label = "λ\n"
    x_label += "Best R={:.3f} at λ={:.3f}".format(optimal_R,
                                                  optimal_lambda)
    box_cox.set_xlabel(x_label)

    # Linearity Plot of the Original Data
    if original_lin_kws is None:
        original_lin_kws = {"title": "Original Data",
                            "show_linear_fitting": True}
    scatter_plot(X, Y, ax=org_lin, show=False, save=False,
                 **original_lin_kws)

    # Linearity Plot of the Transformed Data
    if transformed_lin_kws is None:
        transformed_lin_kws = {"title": "Transformed Data",
                               "show_linear_fitting": True}

    transformed_X = box_cox_transformation(X, optimal_lambda)
    scatter_plot(transformed_X, Y, ax=trans_lin, show=False,
                 save=False, **transformed_lin_kws)

    # Hiding the empty plot in the bottom-right corner
    _.axis("off")

    show_and_save_plot(show=show, save=save,
                       filename="box_cox_linearity_set.png")

    return lambdas, Rs, optimal_lambda, optimal_R
    

def test_box_cox_linearity_plot():
    df = datasets.load_water_density()
    X = df["Temperature"]
    Y = df["Density"]
    box_cox_linearity_plot(X, Y)


def test_box_cox_linearity_set():
    df = datasets.load_water_density()
    X = df["Temperature"]
    Y = df["Density"]
    box_cox_linearity_set(X, Y)


if __name__ == "__main__":
    test_box_cox_linearity_plot()
    test_box_cox_linearity_set()
