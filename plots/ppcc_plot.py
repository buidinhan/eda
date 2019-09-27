"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/ppccplot.htm

Purpose
-------
Graphical Technique for Finding the Shape Parameter of a Distributional
Family that Best Fits a Data Set

The probability plot correlation coefficient (PPCC) plot (Filliben 1975)
is a graphical technique for identifying the shape parameter for a
distributional family that best describes the data set. This technique
is appropriate for families, such as the Weibull, that are defined by a
single shape parameter and location and scale parameters, and it is not
appropriate for distributions, such as the normal, that are defined only
by location and scale parameters.

The PPCC plot is generated as follows. For a series of values for the
shape parameter, the correlation coefficient is computed for the
probability plot associated with a given value of the shape parameter.
These correlation coefficients are plotted against their corresponding
shape parameters. The maximum correlation coefficient corresponds to the
optimal value of the shape parameter. For better precision, two
iterations of the PPCC plot can be generated; the first is for finding
the right neighborhood and the second is for fine tuning the estimate.

The PPCC plot is used first to find a good value of the shape parameter.
The probability plot is then generated to find estimates of the location
and scale parameters and in addition to provide a graphical assessment
of the adequacy of the distributional fit.

Compare Distributions
---------------------
In addition to finding a good choice for estimating the shape parameter
of a given distribution, the PPCC plot can be useful in deciding which
distributional family is most appropriate. For example, given a set of
reliabilty data, you might generate PPCC plots for a Weibull, lognormal,
gamma, and inverse Gaussian distributions, and possibly others, on a
single page. This one page would show the best value for the shape
parameter for several distributions and would additionally indicate
which of these distributional families provides the best fit (as measured
by the maximum probability plot correlation coefficient). That is, if
the maximum PPCC value for the Weibull is 0.99 and only 0.94 for the
lognormal, then we could reasonably conclude that the Weibull family is
the better choice.

Tukey-Lambda PPCC Plot for Symmetric Distributions
--------------------------------------------------
The Tukey Lambda PPCC plot, with shape parameter λ, is particularly
useful for symmetric distributions. It indicates whether a distribution
is short or long tailed and it can further indicate several common
distributions. Specifically,
1. λ = -1: distribution is approximately Cauchy
2. λ = 0: distribution is exactly logistic
3. λ = 0.14: distribution is approximately normal
4. λ = 0.5: distribution is U-shaped
5. λ = 1: distribution is exactly uniform

If the Tukey Lambda PPCC plot gives a maximum value near 0.14, we can
reasonably conclude that the normal distribution is a good model for the
data. If the maximum value is less than 0.14, a long-tailed distribution
such as the double exponential or logistic would be a better choice. If
the maximum value is near -1, this implies the selection of very
long-tailed distribution, such as the Cauchy. If the maximum value is
greater than 0.14, this implies a short-tailed distribution such as the
Beta or uniform.

The Tukey-Lambda PPCC plot is used to suggest an appropriate distribution.
You should follow-up with PPCC and probability plots of the appropriate
alternatives.

Use Judgement When Selecting An Appropriate Distributional Family
-----------------------------------------------------------------
When comparing distributional models, do not simply choose the one with
the maximum PPCC value. In many cases, several distributional fits
provide comparable PPCC values. For example, a lognormal and Weibull may
both fit a given set of reliability data quite well. Typically, we would
consider the complexity of the distribution. That is, a simpler
distribution with a marginally smaller PPCC value may be preferred over
a more complex distribution. Likewise, there may be theoretical
justification in terms of the underlying scientific model for preferring
a distribution with a marginally smaller PPCC value in some cases. In
other cases, we may not need to know if the distributional model is
optimal, only that it is adequate for our purposes. That is, we may be
able to use techniques designed for normally distributed data even if
other distributions fit the data somewhat better.

Sample Plot
-----------
The following is a PPCC plot of 100 normal random numbers. The maximum
value of the correlation coefficient = 0.997 at λ = 0.099.

This PPCC plot shows that:
1. the best-fit symmetric distribution is nearly normal;
2. the data are not long tailed;
3. the sample mean would be an appropriate estimator of location.

We can follow-up this PPCC plot with a normal probability plot to verify
the normality model for the data.

Definition
----------
The PPCC plot is formed by:
* Vertical axis: Probability plot correlation coefficient;
* Horizontal axis: Value of shape parameter.

Questions
---------
The PPCC plot answers the following questions:
1. What is the best-fit member within a distributional family?
2. Does the best-fit member provide a good fit (in terms of generating a
probability plot with a high correlation coefficient)?
3. Does this distributional family provide a good fit compared to other
distributions?
4. How sensitive is the choice of the shape parameter?

Importance
----------
Many statistical analyses are based on distributional assumptions about
the population from which the data have been obtained. However,
distributional families can have radically different shapes depending on
the value of the shape parameter. Therefore, finding a reasonable choice
for the shape parameter is a necessary step in the analysis. In many
analyses, finding a good distributional model for the data is the
primary focus of the analysis. In both of these cases, the PPCC plot is
a valuable tool.

Related Techniques
------------------
* Probability Plot
* Maximum Likelihood Estimation
* Least Squares Estimation
* Method of Moments Estimation
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from utils import datasets
from utils.plotting import show_and_save_plot


def ppcc_plot(x_name, data, lambda_min=-5, lambda_max=5,
              dist="tukeylambda", N=100, ax=None, save=False, show=True):

    if ax is None:
        fig, ax = plt.subplots()

    svals, ppcc = stats.ppcc_plot(data[x_name], lambda_min, lambda_max,
                                  dist=dist, plot=ax, N=N)

    show_and_save_plot(show=show, save=save, filename="ppcc.png")

    max_corr_value = ppcc.max()
    max_corr_lambda = svals[ppcc.argmax()]
    return svals, ppcc, max_corr_value, max_corr_lambda
        

if __name__ == "__main__":
    df = datasets.load_normal()
    _, _, max_c, max_c_l = ppcc_plot("y", df, lambda_min=-2,
                                     lambda_max=2, N=40)
    print("Estimated max correlation coef. = {:.4f} at {:.4f}".format(
                                                        max_c, max_c_l))
