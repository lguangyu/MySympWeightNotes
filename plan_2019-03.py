#!/usr/bin/env python3

import sys
import datetime
import argparse
import wn


def get_args(argv = sys.argv[1:]):
	ap = argparse.ArgumentParser()
	ap.add_argument("-o", "--output",
		type = str, metavar = "png", default = None,
		help = "output to this <png> file")
	args = ap.parse_args(argv)
	return args


class PlanNotes(wn.RecordNotes):
	pass


PlanNotes.add_config(cols = (0, 1), goal = 57.5,
	plot_range = (45, 70), plot_coef = 0.454, plot_label = "WT (kg)"),
PlanNotes.add_config(cols = (2, 3), goal = 67,
	plot_range = (60, 80), plot_coef = 1.000, plot_label = "WS (cm)"),
PlanNotes.add_config(cols = (4, 5), goal = 35,
	plot_range = (30, 40), plot_coef = 1.000, plot_label = "CS (cm)"),
PlanNotes.set_date_range(datetime.date(2019, 1, 5), datetime.date(2019, 3, 31))
PlanNotes.set_date_ticks([
	datetime.date(2019, 1, 5),
	datetime.date(2019, 1, 10),
	datetime.date(2019, 1, 20),
	datetime.date(2019, 2, 1),
	datetime.date(2019, 2, 10),
	datetime.date(2019, 2, 20),
	datetime.date(2019, 3, 1),
	datetime.date(2019, 3, 10),
	datetime.date(2019, 3, 20),
	datetime.date(2019, 3, 31),
])


if __name__ == "__main__":
	args = get_args()
	rn = PlanNotes("plan_2019-03.data.csv")
	if args.output is None:
		rn.plot_and_show()
	else:
		rn.plot_and_save(args.output)
