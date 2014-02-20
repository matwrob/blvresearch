from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt


class FinPlotter:

    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots()

    def plot(self):
        self._initiate_plot()
        self._format_ticks()
        self._format_values()
        self._set_legend()
        plt.show()

    def _set_legend(self):
        fontP = FontProperties()
        fontP.set_size('small')
        legend = self.ax.legend(loc='upper left', shadow=True, prop=fontP)
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        for label in legend.get_texts():
            label.set_fontsize('large')
        for label in legend.get_lines():
            label.set_linewidth(1.5)

    def _initiate_plot(self):
        dates = self.data.index
        for c in self.data.columns:
            self.ax.plot(dates, self.data[c], label=c)

    def _format_ticks(self):
        self.ax.xaxis.set_major_locator(self.years)
        self.ax.xaxis.set_major_formatter(self.yearsFmt)
        self.ax.xaxis.set_minor_locator(self.months)
        self.ax.autoscale_view()

    def _format_values(self):
        self.ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        self.ax.fmt_ydata = self.data
        self.ax.grid(True)
        self.fig.autofmt_xdate()

    @property
    def years(self):
        return YearLocator()

    @property
    def months(self):
        return MonthLocator()

    @property
    def yearsFmt(self):
        return DateFormatter('%Y ')
