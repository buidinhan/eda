import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from utils import datasets
from utils.plotting import show_and_save_plot


def scatter_plot(X, Y, x_label="X", y_label="Y", title=None, x_lim=None,
                 y_lim=None, ax=None, show_linear_fitting=False,
                 show=True, save=False, **kwargs):

    if ax is None:
        fig, ax = plt.subplots(gridspec_kw={"bottom": 0.2},
                               figsize=(6, 4))

    ax.scatter(X, Y, **kwargs)

    if show_linear_fitting:
        slope, intercept, r, p, residual_std = stats.linregress(X, Y)
        ax.plot(X, slope*X+intercept)

        x_label += "\nslope={:.3f}, ".format(slope)
        x_label += "intercept={:.3f}".format(intercept)
        x_label += "\nr={:.3f}, ".format(r)
        x_label += "residual std={:.3f}".format(residual_std)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.set_title(title)

    show_and_save_plot(show=show, save=save, filename="scatter.png")


if __name__ == "__main__":
    df = datasets.load_water_density()
    X = df["Temperature"]
    Y = df["Density"]
    scatter_plot(X, Y, x_label="Temperature", y_label="Density",
                 show_linear_fitting=True, c="green")
