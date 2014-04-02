import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np


def mean_test(event_list, attribute, length):
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    print('Mean:', np.mean(returns))
    # t-test
    # null hypothesis: expected value = 0
    t_statistic, p_value = stats.ttest_1samp(returns, 0)
    print('p_value:', p_value)


def plot_histogram(event_list, attribute, lag=2, length=20):
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    plt.hist(returns, bins=50, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    mu, std = stats.norm.fit(returns)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)


def print_summary_wo_outliers(event_list, attribute, lag=2, length=20,
                              outlier_abs_threshold):
    attribute, length = 'alpha', 20
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
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


def plot_histogram_wo_outliers(event_list, attribute, lag=2, length=20,
                               outlier_abs_threshold):
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
              for e in event_list]
    returns = [s.sum() for s in series
               if abs(s.sum()) < outlier_abs_threshold]
    plt.hist(returns, bins=50, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    mu, std = stats.norm.fit(returns)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
