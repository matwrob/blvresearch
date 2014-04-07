import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np


def mean_test(event_list, attribute, lag, length):
    series = [e.concat_data.series_after(attribute, lag=lag, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    print('Mean:', np.mean(returns))
    # t-test
    # null hypothesis: expected value = 0
    t_statistic, p_value = stats.ttest_1samp(returns, 0)
    print('p_value:', p_value)


def plot_histogram(event_list, attribute, lag, length):
    series = [e.concat_data.series_after(attribute, lag=lag, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    _plot_hist(returns)


def plot_histogram_wo_outliers(event_list, attribute, lag, length,
                               outlier_abs_threshold):
    series = [e.concat_data.series_after(attribute, lag=lag, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    wo_outliers = [r for r in returns if abs(r) < outlier_abs_threshold]
    _plot_hist(wo_outliers)


def _plot_hist(values):
    plt.hist(values, bins=50, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    mu, std = stats.norm.fit(values)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)


def print_summary_wo_outliers(event_list, attribute, lag, length,
                              outlier_abs_threshold):
    series = [e.concat_data.series_after(attribute, lag=lag, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    print('Full sample')
    print('Size:', len(returns))
    print('Mean:', np.mean(returns))
    print(stats.ttest_1samp(returns, 0)[1])
    print()
    wo_outliers = [r for r in returns if abs(r) < outlier_abs_threshold]
    print('Without outliers')
    print('Size: ', len(wo_outliers))
    print('Mean:', np.mean(wo_outliers))
    print(stats.ttest_1samp(wo_outliers, 0)[1])
