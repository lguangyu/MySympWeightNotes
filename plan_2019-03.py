#!/usr/bin/env python3

import wn
import datetime


class PlanNotes(wn.RecordNotes):
	pass

PlanNotes.add_config(cols = (0, 1), goal = 55,
	plot_range = (40, 70), plot_coef = 0.454, plot_label = "WT (kg)"),
PlanNotes.add_config(cols = (2, 3), goal = 66,
	plot_range = (60, 80), plot_coef = 1.000, plot_label = "WS (cm)"),
PlanNotes.add_config(cols = (4, 5), goal = 34,
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
	rn = PlanNotes("plan_2019-03.data.csv")
	rn.plot_and_show()
