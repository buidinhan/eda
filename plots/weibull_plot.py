"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/weibplot.htm

Purpose
-------
Graphical Check To See If Data Come From a Population That Would Be Fit
by a Weibull Distribution

The Weibull plot (Nelson 1982) is a graphical technique for determining
if a data set comes from a population that would logically be fit by a
2-parameter Weibull distribution (the location is assumed to be zero).

The Weibull plot has special scales that are designed so that if the
data do in fact follow a Weibull distribution, the points will be linear
(or nearly linear). The least squares fit of this line yields estimates
for the shape and scale parameters of the Weibull distribution (the
location is assumed to be zero).

Specifically, the shape parameter is the reciprocal of the slope of the
fitted line and the scale parameter is the exponent of the intercept of
the fitted line.

The Weibull distribution also has the property that the scale parameter
falls at the 63.2% point irrespective of the value of the shape parameter.
The plot shows a horizontal line at this 63.2% point and a vertical line
where the horizontal line intersects the least squares fitted line. This
vertical line shows the value of scale parameter.

Sample Plot
-----------
This Weibull plot of the FULLER2.DAT data set shows that:
1. the assumption of a Weibull distribution is reasonable;
2. the scale parameter estimate is computed to be 33.32;
3. the shape parameter estimate is computed to be 5.28; and
4. there are no outliers. 

Note that the values on the x-axis (0, 1, and 2) are the exponents.
These actually denote the value 10^0 = 1, 10^1 = 10, and 10^2 = 100.

Definition
----------
Weibull Cumulative Probability Versus LN(Ordered Response)

The Weibull plot is formed by:
* Vertical axis: Weibull cumulative probability expressed as a percentage
* Horizontal axis: ordered failure times (in a LOG10 scale) 

The vertical scale is ln(-ln(1-p)) where p=(i-0.3)/(n+0.4) and i is the
rank of the observation. This scale is chosen in order to linearize the
resulting plot for Weibull data.

Questions
---------
The Weibull plot can be used to answer the following questions:
1. Do the data follow a 2-parameter Weibull distribution?
2. What is the best estimate of the shape parameter for the 2-parameter
Weibull distribution?
3. What is the best estimate of the scale (= variation) parameter for
the 2-parameter Weibull distribution? 

Importance
----------
Check Distributional Assumptions

Many statistical analyses, particularly in the field of reliability, are
based on the assumption that the data follow a Weibull distribution. If
the analysis assumes the data follow a Weibull distribution, it is
important to verify this assumption and, if verified, find good estimates
of the Weibull parameters.

Related Techniques
------------------
* Weibull Probability Plot
* Weibull PPCC Plot
* Weibull Hazard Plot

The Weibull probability plot (in conjunction with the Weibull PPCC plot),
the Weibull hazard plot, and the Weibull plot are all similar techniques
that can be used for assessing the adequacy of the Weibull distribution
as a model for the data, and additionally providing estimation for the
shape, scale, or location parameters.

The Weibull hazard plot and Weibull plot are designed to handle censored
data (which the Weibull probability plot does not). 
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from utils import datasets
from utils.plotting import show_and_save_plot


def weibull_plot(series, title=None, x_label="log((Measure)",
                 y_label="Weibull Probability", ax=None, show=True,
                 save=False, **kwargs):

    # Calculation of X and Y coordinates and fitting line parameters
    X = np.log(series) / np.log(10)
    X = np.sort(X)

    n = len(series)
    i = np.arange(1, n+1)
    p = (i-0.3) / (n+0.4)
    Y = np.log(-np.log(1-p))

    slope, intercept, r, p_value, error = stats.linregress(X, Y)
    X_for_fitting = np.linspace((-6.908-intercept)/slope, # p=0.001, y=-6.908
                                (1.933-intercept)/slope,  # p=0.999, y=1.933
                                10)
    series_for_fitting = 10 ** X_for_fitting
    Y_for_fitting = intercept + slope*X_for_fitting

    shape_parameter = slope / np.log(10)
    scale_parameter = 10**(-intercept/slope)

    # Plotting
    if ax is None:
        fig, ax = plt.subplots(gridspec_kw={"bottom": 0.2},
                               figsize=(6, 6))
    ax.scatter(series, Y, **kwargs)
    ax.plot(series_for_fitting, Y_for_fitting)
    ax.set_title(title)

    percentage_ticks = np.array([0.1, 0.5, 1, 5, 10, 20, 30, 40, 50,
                                 60, 70, 80, 90, 95, 99, 99.9])
    p_ticks = percentage_ticks / 100
    y_ticks = np.log(-np.log(1-p_ticks))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(percentage_ticks)
    ax.set_ylabel(y_label)
    ax.set_ylim((y_ticks[0], y_ticks[-1]))
    
    ax.set_xscale("log")
    factor = 10**(1/2)
    ax.set_xlim((min(series)/factor, max(series)*factor))
    x_label += "\nr={:.3f}".format(r)
    ax.set_xlabel(x_label)
    
    show_and_save_plot(show=show, save=save, filename="weibull_plot.png")

    return slope, intercept, r, shape_parameter, scale_parameter
    

if __name__ == "__main__":
    df = datasets.load_airplane_glass_failure()
    _, _, _, shape, scale = weibull_plot(df["y"], x_label="log(y)",
                                         c="green")
    print(shape, scale)
