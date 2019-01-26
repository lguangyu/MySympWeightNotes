#!/usr/bin/env python3

import numpy
import datetime
#from . import base as base_m
from . import plot as plot_m


class RecordNotes(plot_m.Plot):
	def __init__(self, fname, *ka, **kw):
		super(RecordNotes, self).__init__(*ka, **kw)
		self.load_data(fname, **kw)


	def load_data(self, fname, *, delimiter = ",", comments = "#", **kw):
		text = numpy.loadtxt(fname, delimiter = delimiter, dtype = object,
			comments = comments, **kw)
		dates = map(lambda i: datetime.datetime.strptime(i, "%Y-%m-%d"), text[:, 0])
		dates = numpy.asarray(list(dates), dtype = object)
		data = text[:, 1:].astype(float)
		#
		self.dates = dates
		self.data = data
		return



