#!/usr/bin/env python3

import numpy
from . import base as base_m


class Plot(base_m.NoteBase):
	matplotlib = None
	_layout_ = dict(
		width = 8, # inches
		left_margin = 0.8, # inches
		right_margin = 0.4, # inches
		top_margin = 0.4, # inches
		bottom_margin = 0.5, # inches
		axes_height = 2.4, # inches
		axes_hspace = 0.09, # axes coords
	)
	_date_range_ = None
	_date_ticks_ = None


	def __init__(self, *ka, **kw):
		super(Plot, self).__init__(*ka, **kw)


	@classmethod
	def _lazy_load_matplotlib(cls):
		if cls.matplotlib is None:
			import matplotlib
			import matplotlib.pyplot
			import matplotlib.dates
			cls.matplotlib = matplotlib
		return


	@classmethod
	def set_date_range(cls, date_start, date_end):
		cls._date_range_ = (date_start, date_end)
		return


	@classmethod
	def set_date_ticks(cls, ticks_list):
		cls._date_ticks_ = ticks_list
		return


	def _setup_figure(self):
		cfgs = self.get_configs()
		layout = self._layout_
		n_plots = len(cfgs)
		width = layout["width"]
		height = layout["axes_height"] *\
			(n_plots + layout["axes_hspace"] * (n_plots - 1))
		figure, axes = self.matplotlib.pyplot.subplots(
			nrows = n_plots, ncols = 1, figsize = (width, height), sharex = True)
		self.matplotlib.pyplot.subplots_adjust(
			left = layout["left_margin"] / width,
			right = 1.0 - layout["right_margin"] / width,
			top = 1.0 - layout["top_margin"] / height,
			bottom = layout["bottom_margin"] / height,
			hspace = layout["axes_hspace"])
		figure.align_ylabels(axes)
		return figure, axes


	def _plot_profile(self, axes, x, data, cfg):
		# appearance
		for sp in axes.spines.values():
			sp.set_visible(False)
		axes.set_facecolor("#F0F0F0")
		axes.grid(linestyle = "-", linewidth = 1.0, color = "#FFFFFF")
		#
		goal = cfg.goal
		cols = cfg.cols
		y = numpy.nanmean(data[:, cols], axis = 1) * cfg.plot_coef
		mask_above = y > goal
		mask_below = y <= goal
		axes.plot(x, y, linestyle = "-", linewidth = 1.5, color = "#4040FF",
			marker = "o", markersize = 4.5, markeredgewidth = 1.0, clip_on = False,
			markeredgecolor = "#4040FF", markerfacecolor = "#FFFFFF")
		for mask, color in zip([mask_above, mask_below], ["#4040FF40", "#40FF4040"]):
			mx = x[mask]
			y1 = numpy.full(len(mx), goal, dtype = float)
			y2 = y[mask]
			if len(mx):
				axes.fill_between(mx, y1 = y1, y2 = y2, facecolor = color)
		axes.axhline(goal, linestyle = "-", linewidth = 1.0, color = "#40FF40")
		#
		axes.set_ylim(*cfg.plot_range)
		axes.set_ylabel(cfg.plot_label)
		axes.set_xlim(*self._date_range_)
		axes.set_xticks(self._date_ticks_)
		xtick_fmt = self.matplotlib.dates.DateFormatter("%b-%d")
		axes.xaxis.set_major_formatter(xtick_fmt)
		return


	def _plot_profiles(self):
		self._lazy_load_matplotlib()
		figure, axes = self._setup_figure()
		x = self.get_dates()
		data = self.get_data()
		for ax, cfg in zip(axes, self.get_configs()):
			self._plot_profile(ax, x = x, data = data, cfg = cfg)
		return


	def plot_and_show(self):
		self._plot_profiles()
		self.matplotlib.pyplot.show()
		self.matplotlib.pyplot.close()
		return
