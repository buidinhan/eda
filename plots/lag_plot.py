"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/lagplot.htm

Purpose: Check for randomness
-----------------------------
A lag plot checks whether a data set or time series is random or not.
Random data should not exhibit any identifiable structure in the lag
plot. Non-random structure in the lag plot indicates that the underlying
data are not random. Several common patterns for lag plots are shown in
the examples below.

Definition
----------
A lag is a fixed time displacement. For example, given a data set Y1,
Y2 ..., Yn, Y2 and Y7 have lag 5 since 7 - 2 = 5. Lag plots can be
generated for any arbitrary lag, although the most commonly used lag is
1.

A plot of lag 1 is a plot of the values of Yi versus Y[i-1]
* Vertical axis: Yi for all i
* Horizontal axis: Y[i-1] for all i

Questions
---------
Lag plots can provide answers to the following questions:
1. Are the data random?
2. Is there serial correlation in the data?
3. What is a suitable model for the data?
4. Are there outliers in the data?

Importance
----------
Inasmuch as randomness is an underlying assumption for most statistical
estimation and testing techniques, the lag plot should be a routine tool
for researchers.

Related Techniques
------------------
* Autocorrelation Plot
* Spectrum
* Runs Test
"""


import pandas as pd
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot


def lag_plot(series, lag=1, ax=None, x_lim=None, y_lim=None,
             title="Lag Plot", show=True, save=False, **kwargs):

    if ax is None:
        fig, ax = plt.subplots()

    pd.plotting.lag_plot(series, lag=lag, ax=ax, **kwargs)
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.set_title(title)
    
    show_and_save_plot(show=show, save=save, filename="lag_plot.png")


def test():
    df = datasets.load_filter_transmittance()
    x_min = df.iloc[:-1, 0].min()
    x_max = df.iloc[:-1, 0].max()
    y_min = df.iloc[1:, 0].min()
    y_max = df.iloc[1:, 0].max()
    d = 0.0002
    lag_plot(df["transmittance"], x_lim=(x_min-d, x_max+d),
             y_lim=(y_min-d, y_max+d), c="green")


if __name__ == "__main__":
    test()
