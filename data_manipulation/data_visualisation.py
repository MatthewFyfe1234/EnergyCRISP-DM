import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO


def demand_over_time(data, title, x_label):
    data['Demand'].plot(marker='.', color='black', alpha=0.5, figsize=(14, 5))
    plt.title(title)
    plt.ylabel('Demand (MW)')
    plt.xlabel(x_label)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(1, 1))
    memfile = BytesIO()
    plt.savefig(memfile)
    return memfile


def sidebyside_stacked_barcharts(data, l_stack_vars, r_stack_vars, title, y_label):
    l_stack_vals, r_stack_vals = [list(data[var]) for var in l_stack_vars], [list(data[var]) for var in r_stack_vars]
    fix, ax = plt.subplots()
    index, width, space = np.arange(len(data)) - 0.17, 0.30, 0.05
    l_y_placement, r_y_placement = [0 for _ in range(len(l_stack_vals[0]))], [0 for _ in range(len(l_stack_vals[0]))]
    l_colours, r_colours = ['black'], ['green', 'blue', 'yellow']
    for i, set_ in enumerate(l_stack_vals):
        ax.bar(index, set_, width, color=l_colours[i], bottom=l_y_placement, label=l_stack_vars[i])
        l_y_placement = [w + o for w, o in zip(set_, l_y_placement)]
    for i, set_ in enumerate(r_stack_vals):
        ax.bar(index + width + space, set_, width, color=r_colours[i], bottom=r_y_placement, label=r_stack_vars[i])
        r_y_placement = [w + o for w, o in zip(set_, r_y_placement)]
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel('Week number')
    plt.legend(loc=2)
    memfile = BytesIO()
    plt.savefig(memfile)
    return memfile


def subplot_line_set(var_set, axis, plot_loc, title, xlabel, ylabel, xrange, legend_set, xtickintervals, data_set=None):
    for var in var_set:
        if data_set is not None:
            axis[plot_loc].plot(data_set[var])
        else:
            axis[plot_loc].plot(var)
        axis[plot_loc].set_title(title)
        axis[plot_loc].set_xlabel(xlabel)
        axis[plot_loc].set_ylabel(ylabel)
        axis[plot_loc].legend(legend_set)
        axis[plot_loc].set_xlim(xrange[0], xrange[1])
        # axis[plot_loc].set_xlim(yrange[0], yrange[1])
        axis[plot_loc].xaxis.set_ticks(np.arange(xtickintervals[0], xtickintervals[1], xtickintervals[2]))
    return axis[plot_loc]
