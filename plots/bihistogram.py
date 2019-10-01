"""
## Source
https://www.itl.nist.gov/div898/handbook/eda/section3/bihistog.htm

##
Purpose
Check for a change in location, variation, or distribution
The bihistogram is an EDA tool for assessing whether a before-versus-after
engineering modification has caused a change in
* location;
* variation; or
* distribution. 

It is a graphical alternative to the two-sample t-test. The bihistogram
can be more powerful than the t-test in that all of the distributional
features (location, scale, skewness, outliers) are evident on a single
plot. It is also based on the common and well-understood histogram.

## Definition
Two adjoined histograms

Bihistograms are formed by vertically juxtaposing two histograms:
* Above the axis: Histogram of the response variable for condition 1
* Below the axis: Histogram of the response variable for condition 2 

## Questions
The bihistogram can provide answers to the following questions:
1. Is a (2-level) factor significant?
2. Does a (2-level) factor have an effect?
3. Does the location change between the 2 subgroups?
4. Does the variation change between the 2 subgroups?
5. Does the distributional shape change between subgroups?
6. Are there any outliers? 

## Importance
Checks 3 out of the 4 underlying assumptions of a measurement process

The bihistogram is an important EDA tool for determining if a factor
"has an effect". Since the bihistogram provides insight into the
validity of three (location, variation, and distribution) out of the
four (missing only randomness) underlying assumptions in a measurement
process, it is an especially valuable tool. Because of the dual
(above/below) nature of the plot, the bihistogram is restricted to
assessing factors that have only two levels. However, this is very
common in the before-versus-after character of many scientific and
engineering experiments.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot
from plots import histogram


def bihistogram(series_1, series_2, labels=["Series 1", "Series_2"],
                bins=10, x_label="Measure", y_label="Count", title=None,
                edgecolor="k", show=True, save=False, **kwargs):

    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True,
                             gridspec_kw={
                                 "left": 0.1, "right": 0.98,
                                 "top": 0.9, "bottom": 0.1,
                                 "wspace": 0.3, "hspace": 0,
                                 },
                             figsize=(6, 6))
    hist_1, hist_2 = axes

    # Calculation of shared bin edges for the 2 histograms
    all_values = np.append(np.array(series_1), np.array(series_2))
    _, bin_edges = np.histogram(all_values, bins=bins)
    
    histogram(series_1, bins=bin_edges, x_label=None, y_label=y_label,
              ax=hist_1, show=False, **kwargs)
    
    histogram(series_2, bins=bin_edges, x_label=x_label, y_label=y_label,
              ax=hist_2, show=False, **kwargs)
    hist_2.invert_yaxis()

    hist_1.annotate(labels[0], xy=(0.02, 0.9), xycoords="axes fraction")
    hist_2.annotate(labels[1], xy=(0.02, 0.05), xycoords="axes fraction")
    fig.suptitle(title)

    show_and_save_plot(show=show, save=save, filename="bihistogram.png")


if __name__ == "__main__":
    df = datasets.load_ceramic_strength()
    batch_1 = df[df["Batch"]==1]["Y"]
    batch_2 = df[df["Batch"]==2]["Y"]
    bihistogram(batch_1, batch_2, labels=["Batch 1", "Batch 2"],
                x_label="Ceramic Strength", bins=20)
