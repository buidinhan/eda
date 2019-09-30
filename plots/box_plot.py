"""
Source
------
https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm

Purpose
-------
Check location and variation shifts

Box plots (Chambers 1983) are an excellent tool for conveying location
and variation information in data sets, particularly for detecting and
illustrating location and variation changes between different groups of
data.

Sample Plot
-----------
This box plot reveals that machine has a significant effect on energy
with respect to location and possibly variation.

This box plot, comparing four machines for energy output, shows that
machine has a significant effect on energy with respect to both location
and variation. Machine 3 has the highest energy response (about 72.5);
machine 4 has the least variable energy response with about 50% of its
readings being within 1 energy unit.

Definition
----------
Box plots are formed by
* Vertical axis: Response variable
* Horizontal axis: The factor of interest

More specifically, we
1. Calculate the median and the quartiles (the lower quartile is the
25th percentile and the upper quartile is the 75th percentile).
2. Plot a symbol at the median (or draw a line) and draw a box (hence
the name--box plot) between the lower and upper quartiles; this box
represents the middle 50% of the data--the "body" of the data.
3. Draw a line from the lower quartile to the minimum point and another
line from the upper quartile to the maximum point. Typically a symbol is
drawn at these minimum and maximum points, although this is optional.

Thus the box plot identifies the middle 50% of the data, the median, and
the extreme points.

Single or multiple box plots can be drawn
-----------------------------------------
A single box plot can be drawn for one batch of data with no distinct
groups. Alternatively, multiple box plots can be drawn together to
compare multiple data sets or to compare groups in a single data set.
For a single box plot, the width of the box is arbitrary. For multiple
box plots, the width of the box plot can be set proportional to the number
of points in the given group or sample (some software implementations of
the box plot simply set all the boxes to the same width).

Box plots with fences
---------------------
There is a useful variation of the box plot that more specifically
identifies outliers. To create this variation:
1. Calculate the median and the lower and upper quartiles.
2. Plot a symbol at the median and draw a box between the lower and
upper quartiles.
3. Calculate the interquartile range (the difference between the upper
and lower quartile) and call it IQ.
4. Calculate the following points:
* L1 = lower quartile - 1.5IQ
* L2 = lower quartile - 3.0IQ
* U1 = upper quartile + 1.5IQ
* U2 = upper quartile + 3.0IQ
5. The line from the lower quartile to the minimum is now drawn from the
lower quartile to the smallest point that is greater than L1. Likewise,
the line from the upper quartile to the maximum is now drawn to the
largest point smaller than U1.
6. Points between L1 and L2 or between U1 and U2 are drawn as small
circles. Points less than L2 or greater than U2 are drawn as large
circles.

Questions
---------
The box plot can provide answers to the following questions:
1. Is a factor significant?
2. Does the location differ between subgroups?
3. Does the variation differ between subgroups?
4. Are there any outliers?

Importance
----------
Check the significance of a factor

The box plot is an important EDA tool for determining if a factor has a
significant effect on the response with respect to either location or
variation.

The box plot is also an effective tool for summarizing large quantities
of information.

Related Techniques
------------------
* Mean Plot
* Analysis of Variance
"""


import pandas as pd
import matplotlib.pyplot as plt

from utils import datasets
from utils.plotting import show_and_save_plot


def box_plot(df, column=None, group=None, x_label=None, y_label=None,
             ax=None, show=True, save=False, **kwargs):

    if ax is None:
        fig, ax = plt.subplots()

    df.boxplot(column=column, by=group, ax=ax, **kwargs)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    show_and_save_plot(show=show, save=save, filename="box_plot.png")


if __name__ == "__main__":
    df = datasets.load_notch_testing()
    box_plot(df, column="Energy", group="Machine", x_label="Machine",
             y_label="Energy", grid=False)
