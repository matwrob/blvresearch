import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import numpy as np


def mean_test(event_list, attribute, lag, length):
    series = [e.concat_data.series_after(attribute, lag=lag, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    miu = np.mean(returns) * 100
    t_stat, p_value = stats.ttest_1samp(returns, 0)  # H0: E[X] = 0
    return(round(miu, 3), p_value)


def tabular_results(list_of_event_lists, attribute, days_combinations):
    result = pd.DataFrame(index=[el.description for el in list_of_event_lists],
                          columns=[c for c in days_combinations])
    for el in list_of_event_lists:
        for c in days_combinations:
            result.loc[el.description][c] = mean_test(el, attribute,
                                                      lag=c[0], length=c[1])
    return result


def print_mean_test(event_list, attribute, lag, length):
    series = [e.concat_data.series_after(attribute, lag=lag, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    miu = np.mean(returns) * 100
    t_stat, p_value = stats.ttest_1samp(returns, 0)  # H0: E[X] = 0
    print('Mean: ', round(miu, 3))
    print('p_value:', p_value)
    print('t_stat:', t_stat)


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
