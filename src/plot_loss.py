import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# from matplotlib.ticker import MultipleLocator

rc('font',**{'family':'sans-serif','sans-serif':['DejaVu Sans'],'size':12})
# Set the font used for MathJax - more on this later
rc('mathtext',**{'default':'regular'})
rc('axes',**{'titlesize': 15})

def load_from_file(filename, delimiter, skiprows=0):
    data = np.loadtxt(open(filename, "rb"), delimiter=delimiter, skiprows=skiprows)
    return data[:,0], data[:,1], data[:,2], data[:,3]

def plot_fig(ax, x, y, marker, color, label='', alpha=1, edgecolor='black', markersize=8):
    ax.plot(
        x, y,   # data
        marker=marker,     # marker style
        markersize=markersize,   # marker size
        markerfacecolor=color,   # marker facecolor
        markeredgecolor=edgecolor,  # marker edgecolor
        markeredgewidth=2,       # marker edge width
        linestyle='-',            # line style
        color=color,     # line color
        linewidth=3,      # line width
        label=label,      # dataset label
        alpha=alpha       # transparency
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input_file", type=str, default="./data/losses.txt")
    parser.add_argument("--out_name", type=str, default="./out.png")

    args, _ = parser.parse_known_args()
    input_file = args.input_file
    output_file = args.out_name

    # fig = plt.figure(figsize=(10,6))
    # ax = fig.add_axes([0.1,0.1,0.5,0.8])
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,4))

    iter, elec_loss, flow_loss, total_loss = load_from_file(input_file, "\t", 1)

    plot_fig(ax, iter, elec_loss, None, 'blue', 'Electric loss', 1.0, 'black', 5)
    plot_fig(ax, iter, flow_loss, None, 'red', 'Flow loss', 1.0, 'black', 5)
    plot_fig(ax, iter, total_loss, None, 'green', 'Total loss', 1.0, 'black', 5)
    ax.set_title("Objective function")

    ax.set_ylim(0, 2.0)
    # ax.set_xlim(0, 50)
    ax.set_ylabel("Normalized loss")
    ax.set_xlabel("Iteration number")
    # axes.yaxis.set_major_locator(MultipleLocator(50))
    # axes.yaxis.set_minor_locator(MultipleLocator(50))
    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    # plt.show()
