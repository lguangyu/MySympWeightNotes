#!/usr/bin/env python3


class Namespace(object):
	def __init__(self, *ka, **kw):
		super(Namespace, self).__init__()


class ColumnConfig(Namespace):
	def __init__(self, cols, goal, *ka,
		plot_range = (0, 100), plot_coef = 1.0, plot_label = "", **kw):
		super(ColumnConfig, self).__init__(*ka, **kw)
		self.cols = cols
		self.goal = goal
		self.plot_range = plot_range
		self.plot_coef = plot_coef
		self.plot_label = plot_label


class NoteBase(Namespace):
	_column_configs_ = []

	def __init__(self, *ka, **kw):
		super(NoteBase, self).__init__()


	@classmethod
	def add_config(cls, *ka, **kw):
		cfg = ColumnConfig(*ka, **kw)
		cls._column_configs_.append(cfg)


	@classmethod
	def get_configs(cls):
		return cls._column_configs_


	def get_dates(self):
		return self.dates


	def get_data(self):
		return self.data

