"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/autocopl.htm

Purpose
-------
Check Randomness

Autocorrelation plots (Box and Jenkins, pp. 28-32) are a commonly-used
tool for checking randomness in a data set. This randomness is
ascertained by computing autocorrelations for data values at varying
time lags. If random, such autocorrelations should be near zero for any
and all time-lag separations. If non-random, then one or more of the
autocorrelations will be significantly non-zero.

In addition, autocorrelation plots are used in the model identification
stage for Box-Jenkins autoregressive, moving average time series models.

Autocorrelation is Only One Measure of Randomness
-------------------------------------------------
Note that uncorrelated does not necessarily mean random. Data that has
significant autocorrelation is not random. However, data that does not
show significant autocorrelation can still exhibit non-randomness in
other ways. Autocorrelation is just one measure of randomness. In the
context of model validation (which is the primary type of randomness we
dicuss in the Handbook), checking for autocorrelation is typically a
sufficient test of randomness since the residuals from a poor fitting
models tend to display non-subtle randomness. However, some applications
require a more rigorous determination of randomness. In these cases, a
battery of tests, which might include checking for autocorrelation, are
applied since data can be non-random in many different and often subtle
ways.

An example of where a more rigorous check for randomness is needed would
be in testing random number generators.

Sample Plot
-----------
Autocorrelations should be near-zero for randomness. Such is not the
case in this example and thus the randomness assumption fails.

This sample autocorrelation plot of the FLICKER.DAT data set shows that
the time series is not random, but rather has a high degree of
autocorrelation between adjacent and near-adjacent observations.

Definition
----------
r(h) versus h

Autocorrelation plots are formed by
* Vertical axis: Autocorrelation coefficient R[h]=C[h]/C[0], where C[h]
is the autocovariance function
    C[h] =(1/N) * ∑((Y[t] − Ybar)*(Y[t+h] − Ybar)) for t = 1 to N-h
and C[0] is the variance function
    C[0] = (1/N) * ∑(Y[t] − Ybar)^2 for t = 1 to N.
Note that R[h] is between -1 and +1. Note that some sources may use the
following formula for the autocovariance function
    C[h] =1/(N−h) * ∑((Y[t] − Ybar)*(Y[t+h] − Ybar)) for t = 1 to N-h.
Although this definition has less bias, the (1/N) formulation has some
desirable statistical properties and is the form most commonly used in
the statistics literature. See pages 20 and 49-50 in Chatfield for
details.

* Horizontal axis: Time lag h (h = 1, 2, 3, ...)
* The above plot also contains several horizontal reference lines. The
middle line is at zero. The other four lines are 95% and 99% confidence
bands. Note that there are two distinct formulas for generating the
confidence bands.
1. If the autocorrelation plot is being used to test for randomness
(i.e., there is no time dependence in the data), the following formula
is recommended: ± z(1−α/2) / √N, where N is the sample size, z is the
cumulative distribution function of the standard normal distribution
and α is the significance level. In this case, the confidence bands
have fixed width that depends on the sample size. This is the formula
that was used to generate the confidence bands in the above plot.
2. Autocorrelation plots are also used in the model identification stage
for fitting ARIMA models. In this case, a moving average model is
assumed for the data and the following confidence bands should be
generated:
    ± z(1−α/2) * √(1/N) * √(1 + 2 * ∑ y[i]^2 for i = 1 to k)),
where k is the lag, N is the sample size, z is the cumulative distribution
function of the standard normal distribution and α is the significance
level. In this case, the confidence bands increase as the lag increases.

Questions
---------
The autocorrelation plot can provide answers to the following questions:
1. Are the data random?
2. Is an observation related to an adjacent observation?
3. Is an observation related to an observation twice-removed? (etc.)
4. Is the observed time series white noise?
5. Is the observed time series sinusoidal?
6. Is the observed time series autoregressive?
7. What is an appropriate model for the observed time series?
8. Is the model Y = constant + error valid and sufficient?
9. Is the formula s[Ybar] = s / √N valid?

Importance
----------
Ensure validity of engineering conclusions 	

Randomness (along with fixed model, fixed variation, and fixed distribution)
is one of the four assumptions that typically underlie all measurement
processes. The randomness assumption is critically important for the
following three reasons:
1. Most standard statistical tests depend on randomness. The validity of
the test conclusions is directly linked to the validity of the randomness
assumption.
2. Many commonly-used statistical formulae depend on the randomness
assumption, the most common formula being the formula for determining
the standard deviation of the sample mean:s[Ybar] = s / √N, where s is
the standard deviation of the data. Although heavily used, the results
from using this formula are of no value unless the randomness assumption
holds.
3. For univariate data, the default model is Y = constant + error. If
the data are not random, this model is incorrect and invalid, and the
estimates for the parameters (such as the constant) become nonsensical
and invalid. 

In short, if the analyst does not check for randomness, then the validity
of many of the statistical conclusions becomes suspect. The autocorrelation
plot is an excellent way of checking for such randomness.

Related Techniques
------------------
* Partial Autocorrelation Plot
* Lag Plot
* Spectral Plot
* Seasonal Subseries Plot
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from utils import datasets
from utils.plotting import show_and_save_plot


def autocovariance(series, lag):
    N = len(series)
    mean = np.mean(series)

    Y = np.array(series)

    if lag == 0:
        return np.mean((Y-mean)**2)
    else:
        return np.sum((Y[:N-lag]-mean)*(Y[lag:]-mean)) / N


def autocorrelation_coefficient(series, lag):
    if lag == 0:
        return 1
    else:
        return autocovariance(series, lag) / autocovariance(series, 0)


def autocorrelation_plot(series, max_lag=None, title=None, ax=None,
                         arima=False, show=True, save=False, **kwargs):

    series = np.array(series)

    if max_lag is None:
        max_lag = len(series)-2 # Lag values of N and N-1 are meaningless.
        
    if ax is None:
        fig, ax = plt.subplots()

    # Plotting autocorrelation coefficients
    lags = range(0, max_lag+1)
    coefs = [autocorrelation_coefficient(series, lag) for lag in lags]

    ax.plot(lags, coefs, **kwargs)
    ax.set_title(title)
    ax.set_xlabel("Lag")
    ax.set_ylabel("Autocorrelation Coefficient")
    ax.set_ylim((-1, 1))

    # Plotting confidence lines
    z_95 = stats.norm.ppf(0.975) # 0.975 = 1 - 0.05/2
    z_99 = stats.norm.ppf(0.995) # 0.995 = 1 - 0.01/2
    N = len(series)

    if arima:
        confidence_95 = np.array(
            [z_95/np.sqrt(N)*np.sqrt(1+2*np.sum(series[0:lag]**2))
            for lag in lags])
        confidence_99 = np.array(
            [z_99/np.sqrt(N)*np.sqrt(1+2*np.sum(series[0:lag]**2))
            for lag in lags])
        ax.plot(lags, confidence_99, c="k")
        ax.plot(lags, confidence_95, c="k")
        ax.plot(lags, -confidence_95, c="k")
        ax.plot(lags, -confidence_99, c="k")
    else:
        confidence_95 = z_95 / np.sqrt(N)
        confidence_99 = z_99 / np.sqrt(N)
        ax.axhline(y=confidence_99)
        ax.axhline(y=confidence_95)
        ax.axhline(y=-confidence_95)
        ax.axhline(y=-confidence_99)

    show_and_save_plot(show=show, save=save, filename="autocorrelation.png")

    return coefs, confidence_95, confidence_99


if __name__ == "__main__":
    df = datasets.load_flicker_noise()
    
    coefs, _, _ = autocorrelation_plot(df["y"], max_lag=250, arima=True,
                                       c="green", marker=".", alpha=0.5)

    for lag, coef in enumerate(coefs[:20]):
        print("lag={:>2}, autocorrelation={:.4f}".format(lag, coef))
