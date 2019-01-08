#!/usr/bin/env python3

import numpy
from matplotlib import pyplot
import matplotlib.dates
import sys
import argparse
import datetime


PLOT_GROUP_CONFIGS = [
	dict(cols = (0, 1), goal = 55, ylim = (40, 70), coef = 0.454, ylabel = "WT (kg)"),
	dict(cols = (2, 3), goal = 66, ylim = (60, 80), coef = 1.000, ylabel = "WS (cm)"),
	dict(cols = (4, 5), goal = 34, ylim = (30, 40), coef = 1.000, ylabel = "LLC (cm)"),
]

START_DATE = datetime.date(2019, 1, 4)
END_DATE = datetime.date(2019, 3, 20)
DATE_DELTA = datetime.timedelta(days = 15)


def get_args():
	ap = argparse.ArgumentParser()
	ap.add_argument("input", type = str, help = "input data file")
	ap.add_argument("-o", "--output", type = str, metavar = "png", default = None,
		help = "specify an output png file, or '-' write to stdout (default: open matplotlib interactive window")
	return ap.parse_args()


def parse_data_file(fname):
	with open(fname, "r") as fh:
		txt = [i.split(",") for i in fh.read().splitlines()]
	dates = numpy.asarray([datetime.datetime.strptime(i[0], "%Y-%m-%d") for i in txt],
		dtype = object)
	data = numpy.asarray([i[1:] for i in txt], dtype = float)
	# lbs to kg
	return dates, data


def date_range(start, end, step):
	ret = []
	i = start
	while i < end:
		ret.append(i)
		i = i + step
	return ret


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
	y = numpy.nanmean(data[:, cols], axis = 1) * cfg["coef"]
	mask_above = y > goal
	mask_below = y <= goal
	ax.plot(x, y, linestyle = "-", linewidth = 1.5, color = "#4040FF",
		marker = "o", markersize = 4.5, markeredgewidth = 1.0,
		markeredgecolor = "#4040FF", markerfacecolor = "#FFFFFF")
	for mask, color in zip([mask_above, mask_below], ["#4040FF40", "#40FF4040"]):
		mx = x[mask]
		y1 = numpy.full(len(mx), goal, dtype = float)
		y2 = y[mask]
		if len(mx):
			ax.fill_between(mx, y1 = y1, y2 = y2, facecolor = color)
	ax.axhline(goal, linestyle = "-", linewidth = 1.0, color = "#40FF40")
	#
	ax.set_xlim(START_DATE, END_DATE)
	ax.set_ylim(*cfg["ylim"])
	ax.set_ylabel(cfg["ylabel"])
	#ax.set_xticks(date_range(START_DATE, END_DATE, DATE_DELTA))
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
