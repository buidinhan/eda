"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/boxcox.htm

Purpose
-------
Find transformation to normalize data
Many statistical tests and intervals are based on the assumption of
normality. The assumption of normality often leads to tests that are
simple, mathematically tractable, and powerful compared to tests that do
not make the normality assumption. Unfortunately, many real data sets
are in fact not normal. However, an appropriate transformation of a data
set can often yield a data set that does follow a normal distribution.
This increases the applicability and usefulness of statistical techniques
based on the normality assumption.

The Box-Cox transformation is a particulary useful family of
transformations. It is defined as: T(X) = (X^λ - 1) / λ, where X is the
response variable and λ is the transformation parameter. For λ = 0, the
log of the data is taken instead of using the above formula.

Given a particular transformation, it is helpful to define a measure of
the normality of the resulting transformation. One measure is to compute
the correlation coefficient of a normal probability plot. The correlation
is computed between the vertical and horizontal axis variables of the
probability plot and is a convenient measure of the linearity of the
probability plot (the more linear the probability plot, the better a
normal distribution fits the data).

The Box-Cox normality plot is a plot of these correlation coefficients
for various values of the lambda parameter. The value of lambda
corresponding to the maximum correlation on the plot is then the optimal
choice for λ.

Sample Plot
-----------
The histogram in the upper left-hand shows a data set that has significant
right skewness (and so does not follow a normal distribution). The Box-Cox
normality plot shows that the maximum value of the correlation coefficient
is at λ = -0.3. The histogram of the data after applying the Box-Cox
transformation with λ = -0.3 shows a data set for which the normality
assumption is reasonable. This is verified with a normal probability
plot of the transformed data.

Definition
----------
Box-Cox normality plots are formed by:
* Vertical axis: Correlation coefficient from the normal probability
plot after applying Box-Cox transformation
* Horizontal axis: Value for λ

Questions
---------
The Box-Cox normality plot can provide answers to the following
questions:
1. Is there a transformation that will normalize my data?
2. What is the optimal value of the transformation parameter?

Importance
----------
Normalization improves validity of tests

Normality assumptions are critical for many univariate intervals and
tests. It is important to test this normality assumption. If the data
are in fact not normal, the Box-Cox normality plot can often be used to
find a transformation that will normalize the data.

Related Techniques
------------------
* Normal Probability Plot
* Box-Cox Linearity Plot
"""


from functools import partial

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from utils import datasets
from utils.calculations import box_cox_transformation
from utils.plotting import show_and_save_plot
from plots import histogram, probability_plot


def box_cox_normality_plot(series, lambda_min=-2, lambda_max=2, N=100,
                           ax=None, show=True, save=False):

    if ax is None:
        fig, ax = plt.subplots()

    lambdas, corrs = stats.boxcox_normplot(series, lambda_min,
                                           lambda_max, plot=ax, N=N)

    max_corr_value = corrs.max()
    max_corr_lambda = lambdas[corrs.argmax()]

    show_and_save_plot(show=show, save=save,
                       filename="box_cox_normality.png")

    return lambdas, corrs, max_corr_lambda, max_corr_value


def box_cox_normality_set(series, main_title=None, show=True,
                          save=False, box_cox_kws= None, prob_kws=None,
                          original_hist_kws=None,
                          transformed_hist_kws=None):

    fig, axes = plt.subplots(nrows=2, ncols=2,
                             gridspec_kw={
                                 "left": 0.1, "right": 0.98,
                                 "bottom": 0.1, "top": 0.9,
                                 "wspace": 0.3, "hspace": 0.4,
                                 },
                             figsize=(7, 8))
    org_hist, box_cox = axes[0]
    trans_hist, prob = axes[1]

    fig.suptitle(main_title)
    
    # Box-Cox Normality Plot
    if box_cox_kws is None:
        box_cox_kws = {"lambda_min": -2, "lambda_max": 2, "N": 100}
        
    lambdas, corrs, optimal_lambda, max_corr = \
             box_cox_normality_plot(series, ax=box_cox, show=False,
                                    save=False, **box_cox_kws)
    
    x_label = "λ\nMax CC = {:.3f} at λ = {:.3f}".format(max_corr,
                                                  optimal_lambda)
    box_cox.set_xlabel(x_label)

    # Histogram of the Original Data
    if original_hist_kws is None:
        original_hist_kws = {"title": "Original Data"}

    histogram(series, ax=org_hist, show=False, save=False,
              **original_hist_kws)

    # Transformation of Data
    transformed_series = pd.Series(map(partial(box_cox_transformation,
                                               lambda_=optimal_lambda),
                                      series))
    
    # Histogram of the Transformed Data
    if transformed_hist_kws is None:
        transformed_hist_kws = {"title": "Transformed Data",
                                "x_label": "Transformed Measure"}
    
    histogram(transformed_series, ax=trans_hist, show=False, save=False,
              **transformed_hist_kws)

    # Probability Plot of the Transformed Data
    if prob_kws is None:
        prob_kws = {"title": "Probability Plot"}
    probability_plot(series, ax=prob, show=False, save=False, **prob_kws)
    
    show_and_save_plot(show=show, save=save,
                       filename="box_cox_normality_set.png")

    return lambdas, corrs, optimal_lambda, max_corr
    
                          
def test_box_cox_plot():
    df = datasets.load_alaska_pipeline()
    _, _, max_c_l, max_c = box_cox_normality_plot(
                           df["In-Field Defect Size"], N=80)
    print("Estimated max corr. coef. = {:.3f} at λ = {:.3f}".format(
                                                    max_c, max_c_l))


def test_box_cox_set():
    df = datasets.load_michelson()
    box_cox_normality_set(df["light_speed"])


if __name__ == "__main__":
    test_box_cox_set()
