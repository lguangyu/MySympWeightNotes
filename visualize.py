#!/usr/bin/env python3

import numpy
from matplotlib import pyplot
import sys
import argparse
import datetime


PLOT_GROUP_CONFIGS = [
	dict(cols = (0, 1), goal = 55, ylim = (40, 70), ylabel = "WT (kg)"),
	dict(cols = (2, 3), goal = 66, ylim = (60, 80), ylabel = "WS (cm)"),
	dict(cols = (4, 5), goal = 34, ylim = (30, 40), ylabel = "LLC (cm)"),
]


def get_args():
	ap = argparse.ArgumentParser()
	ap.add_argument("input", type = str, help = "input data file")
	ap.add_argument("-o", "--output", type = str, metavar = "png", default = None,
		help = "specify an output png file, or '-' write to stdout (default: open matplotlib interactive window")
	return ap.parse_args()


def parse_data_file(fname):
	with open(fname, "r") as fh:
		txt = [i.split("\t") for i in fh.read().splitlines()]
	dates = numpy.asarray([datetime.datetime.strptime(i[0], "%Y-%m-%d") for i in txt],
		dtype = object)
	data = numpy.asarray([i[1:] for i in txt], dtype = float)
	return dates, data


def hdl_plot(dates, data):
	figure, axes = pyplot.subplots(nrows = len(PLOT_GROUP_CONFIGS), ncols = 1,
		figsize = (8, 8), sharex = True)
	pyplot.subplots_adjust(hspace = 0)
	for ax, cfg in zip(axes, PLOT_GROUP_CONFIGS):
		plot_tracking(ax, dates, data, cfg)
	figure.tight_layout()
	return


def plot_tracking(ax, x, data, cfg):
	goal = cfg["goal"]
	cols = cfg["cols"]
	#
	y = numpy.nanmean(data[:, cols], axis = 1)
	mask_above = y > goal
	mask_below = y <= goal
	ax.plot(x, y, linestyle = "-", linewidth = 1.5, color = "#4040FF",
		marker = "o", markeredgewidth = 1.0, markeredgecolor = "#4040FF", markerfacecolor = "#FFFFFF")
	ax.fill_between(x[mask_above], y1 = goal, y2 = y[mask_above], facecolor = "#4040FF40")
	ax.fill_between(x[mask_below], y1 = goal, y2 = y[mask_below], facecolor = "#40FF4040")
	ax.axhline(goal, linestyle = "-", linewidth = 1.0, color = "#A0A0A080")
	#
	ax.set_ylim(cfg["ylim"])
	ax.set_ylabel(cfg["ylabel"])
	return


def finish_plot(output):
	if output is None:
		pyplot.show()
	elif output == "-":
		pyplot.savefig(sys.stdout.buffer)
	else:
		pyplot.savefig(output)
	return
	

if __name__ == "__main__":
	args = get_args()
	dates, data = parse_data_file(args.input)
	hdl_plot(dates, data)
	finish_plot(args.output)
	pyplot.close()
