"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/4plot.htm

Purpose
-------
Check Underlying Statistical Assumptions

The 4-plot is a collection of 4 specific EDA graphical techniques whose
purpose is to test the assumptions that underlie most measurement
processes. A 4-plot consists of a
1. run sequence plot;
2. lag plot;
3. histogram;
4. normal probability plot. 

If the 4 underlying assumptions of a typical measurement process hold,
then the above 4 plots will have a characteristic appearance (see the
normal random numbers case study below); if any of the underlying
assumptions fail to hold, then it will be revealed by an anomalous
appearance in one or more of the plots. Several commonly encountered
situations are demonstrated in the case studies below.

Although the 4-plot has an obvious use for univariate and time series
data, its usefulness extends far beyond that. Many statistical models
of the form Yi=f(X1,...,Xk)+Ei have the same underlying assumptions for
the error term. That is, no matter how complicated the functional fit,
the assumptions on the underlying error term are still the same. The
4-plot can and should be routinely applied to the residuals when fitting
models regardless of whether the model is simple or complicated.

Sample Plot
-----------
Process Has Fixed Location, Fixed Variation, Non-Random (Oscillatory),
Non-Normal U-Shaped Distribution, and Has 3 Outliers.

This 4-plot of the LEW.DAT data set reveals the following:
1. the fixed location assumption is justified as shown by the run
sequence plot in the upper left corner.
2. the fixed variation assumption is justified as shown by the run
sequence plot in the upper left corner.
3. the randomness assumption is violated as shown by the non-random
(oscillatory) lag plot in the upper right corner.
4. the assumption of a common, normal distribution is violated as shown
by the histogram in the lower left corner and the normal probability
plot in the lower right corner. The distribution is non-normal and is a
U-shaped distribution.
5. there are several outliers apparent in the lag plot in the upper right
corner. 

Definition
----------
The 4-plot consists of the following:
1. Run sequence plot to test fixed location and variation.
* Vertically: Yi
* Horizontally: i 
2. Lag Plot to test randomness.
* Vertically: Yi
* Horizontally: Yi-1 
3. Histogram to test (normal) distribution.
* Vertically: Counts
* Horizontally: Y 
4. Normal probability plot to test normal distribution.
* Vertically: Ordered Yi
* Horizontally: Theoretical values from a normal N(0,1) distribution
for ordered Yi 

Questions
---------
4-plots can provide answers to many questions:
1. Is the process in-control, stable, and predictable?
2. Is the process drifting with respect to location?
3. Is the process drifting with respect to variation?
4. Are the data random?
5. Is an observation related to an adjacent observation?
6. If the data are a time series, is is white noise?
7. If the data are a time series and not white noise, is it sinusoidal,
autoregressive, etc.?
8. If the data are non-random, what is a better model?
9. Does the process follow a normal distribution?
10. If non-normal, what distribution does the process follow?
11. Is the model Yi = A0 + Eivalid and sufficient?
12. If the default model is insufficient, what is a better model?
13. Is the formula s[Y-bar] = s/√N valid?
14. Is the sample mean a good estimator of the process location?
15. If not, what would be a better estimator?
16. Are there any outliers? 

Importance
----------
Testing Underlying Assumptions Helps Ensure the Validity of the Final
Scientific and Engineering Conclusions

There are 4 assumptions that typically underlie all measurement
processes; namely, that the data from the process at hand "behave like":
1. random drawings;
2. from a fixed distribution;
3. with that distribution having a fixed location; and
4. with that distribution having fixed variation. 

Predictability is an all-important goal in science and engineering. If
the above 4 assumptions hold, then we have achieved probabilistic
predictability--the ability to make probability statements not only
about the process in the past, but also about the process in the future.
In short, such processes are said to be "statistically in control". If
the 4 assumptions do not hold, then we have a process that is drifting
(with respect to location, variation, or distribution), is unpredictable,
and is out of control. A simple characterization of such processes by a
location estimate, a variation estimate, or a distribution "estimate"
inevitably leads to optimistic and grossly invalid engineering
conclusions.

Inasmuch as the validity of the final scientific and engineering
conclusions is inextricably linked to the validity of these same 4
underlying assumptions, it naturally follows that there is a real
necessity for all 4 assumptions to be routinely tested. The 4-plot (run
sequence plot, lag plot, histogram, and normal probability plot) is seen
as a simple, efficient, and powerful way of carrying out this routine
checking.

Interpretation
--------------
Flat, Equi-Banded, Random, Bell-Shaped, and Linear

Of the 4 underlying assumptions:
1. If the fixed location assumption holds, then the run sequence plot
will be flat and non-drifting.
2. If the fixed variation assumption holds, then the vertical spread in
the run sequence plot will be approximately the same over the entire
horizontal axis.
3. If the randomness assumption holds, then the lag plot will be
structureless and random.
4. If the fixed distribution assumption holds (in particular, if the
fixed normal distribution assumption holds), then the histogram will be
bell-shaped and the normal probability plot will be approximately linear.

If all 4 of the assumptions hold, then the process is "statistically in
control". In practice, many processes fall short of achieving this ideal.

Related Techniques
* Run Sequence Plot
* Lag Plot
* Histogram
* Normal Probability Plot
* Autocorrelation Plot
* Spectral Plot
* PPCC Plot
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot
from plots import (run_sequence_plot, lag_plot, histogram,
                   probability_plot)


def four_plot(series, main_title="4-PLOT", show=True, save=False,
              run_kws=None, lag_kws=None, hist_kws=None, prob_kws=None):

    fig, axes = plt.subplots(nrows=2, ncols=2,
                             gridspec_kw={
                                 "left": 0.1, "right": 0.98,
                                 "top": 0.9, "bottom": 0.1,
                                 "wspace": 0.3, "hspace": 0.3,
                                 },
                             figsize=(7, 8))
    rsp, lag = axes[0]
    hist, prob = axes[1]
    
    # Run Sequence Plot
    run_kws = run_kws if run_kws is not None else {}
    clearance = (max(series)-min(series)) * 1/10
    y_lim = (min(series)-clearance, max(series)+clearance)
    run_sequence_plot(series, y_lim=y_lim, ax=rsp, show=False, **run_kws)

    # Lag Plot
    lag_kws = lag_kws if lag_kws is not None else {}
    lag_plot(series, ax=lag, show=False, **lag_kws)
    
    # Histogram
    hist_kws = hist_kws if hist_kws is not None else {}
    histogram(series, ax=hist, show=False, **hist_kws)

    # Probability Plot
    prob_kws = prob_kws if prob_kws is not None else {}
    probability_plot(series, ax=prob, show=False, **prob_kws)
    
    fig.suptitle(main_title)
    
    show_and_save_plot(show=show, save=save, filename="4-plot.png")


def test():
    df = datasets.load_beam_deflection()
    four_plot(df["Deflection"], run_kws={"title": "Run Sequence Plot",
                                         "y_label": "Deflection"},
              hist_kws={"bins": 20, "title": "Histogram",
                        "x_label": "Deflection"},
              prob_kws={"title": "Normality Plot"})


if __name__ == "__main__":
    test()
