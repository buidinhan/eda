import matplotlib.pyplot as plt


def show_and_save_plot(show=True, save=False, filename="plot.png"):
    plt.gcf()

    if save:
        plt.savefig(filename)

    if show:
        plt.show()
