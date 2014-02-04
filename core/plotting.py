from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.pyplot as plt
import pandas as pd

from concat.core.utils import load_object, namespace


class FinPlotter:

    def __init__(self, data, list_of_columns_to_plot=None):
        self.to_plot = list_of_columns_to_plot
        self.data = data
        self.plot_type = self._determine_plot_type()
        self.fig, self.ax = plt.subplots()

    def plot(self):
        self._initiate_plot()
        self._format_ticks()
        self._format_values()
        plt.show()

    def _initiate_plot(self):
        if self.plot_type == 'dataframe':
            raise NotImplementedError('cannot plot more than a single series')
        else:
            dates = self.data.index
            values = self.data.values
        self.ax.plot_date(dates, values, '-')

    def _format_ticks(self):
        self.ax.xaxis.set_major_locator(self.years)
        self.ax.xaxis.set_major_formatter(self.yearsFmt)
        self.ax.xaxis.set_minor_locator(self.months)
        self.ax.autoscale_view()

    def _format_values(self):
        self.ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        self.ax.fmt_ydata = price
        self.ax.grid(True)
        self.fig.autofmt_xdate()

    def _determine_plot_type(self):
        result = 'dataframe' if self.to_plot else 'series'
        return result

    @property
    def years(self):
        return YearLocator()

    @property
    def months(self):
        return MonthLocator()

    @property
    def yearsFmt(self):
        return DateFormatter('%Y ')


def plot_financial_series(series):
    fig, ax = plt.subplots()
    years    = YearLocator()   # every year
months   = MonthLocator()  # every month
yearsFmt = DateFormatter('%Y')

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()

