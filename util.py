import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict
import os
import seaborn as sns
import itertools
import tikzplotlib as tikz


SMALL_SIZE = 14
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # font-size of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # font-size of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # font-size of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # font-size of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend font-size
plt.rc('figure', titlesize=BIGGER_SIZE)  # font-size of the figure title


class SimulationConfiguration:
    def __init__(self, r2r_balance, r2c_balance, base_fee, proportional_fee):
        self.r2r_balance = r2r_balance
        self.r2c_balance = r2c_balance
        self.base_fee = base_fee
        self.proportional_fee = proportional_fee

    def __hash__(self):
        return hash((self.r2c_balance, self.r2c_balance, self.base_fee, self.proportional_fee))

    def __eq__(self, other):
        return (self.r2r_balance, self.r2c_balance, self.base_fee, self.proportional_fee) \
               == (other.r2r_balance, other.r2c_balance, other.base_fee, other.proportional_fee)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __str__(self):
        return "{}%".format(self.proportional_fee * 100)


def store_results(results: Dict[SimulationConfiguration, List[float]], filepath, filename, csv=False) -> pd.DataFrame:
    """

    :param csv:
    :param filepath:
    :param results:
    :param filename:
    :return:
    """
    df = pd.DataFrame.from_dict(results)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    if csv:
        df.to_csv(os.path.join(filepath, filename + '.csv'), index=False)
    else:
        df.to_pickle(os.path.join(filepath, filename + '.pickle'))
    return df


def plot_graphs(dfs,
                plot_path,
                ylabels: List[str] = None,
                titles: List[str] = None,
                plot_names: List[str] = None,
                subtitles: List[str] = None,
                plot=False):
    """

    :param dfs:
    :param plot_path:
    :param ylabels:
    :param titles:
    :param plot_names:
    :return:
    """
    if type(dfs) is not list:
        dfs = [dfs]

    if ylabels is None:
        ylabels = ["Result" for _ in range(len(dfs))]

    if titles is None:
        titles = [str(i) for i in range(len(dfs))]

    if plot_names is None:
        plot_names = titles

    for df, ylabel, title, name, subtitle in zip(dfs, ylabels, titles, plot_names, subtitles):
        df.plot(title=title + "\n" + subtitle, figsize=(20, 10))\
            .legend(loc="upper left", frameon=True, framealpha=0.7, ncol=1, shadow=False, borderpad=1,
                    title='Proportional Fees in percent')
        plt.title(title + "\n" + subtitle, fontsize=20)
        plt.ylabel(ylabel)
        plt.xlabel('Transaction Number')
        plt.savefig(fname=os.path.join(plot_path, name + '.png'))
        tikz.save(os.path.join(plot_path, name + '.tex'), encoding='utf-8')
        if plot:
            plt.show()
    plt.close('all')


def plot_histogram(df: pd.DataFrame, plot_path, title, name, labels, subtitle, plot=False):
    """

    :param df:
    :param plot_path:
    :param title:
    :param name:
    :param labels:
    :param plot:
    :return:
    """
    df.plot.bar(figsize=(20, 10))\
        .legend(loc="upper left", frameon=True, framealpha=0.7, ncol=1, shadow=False, borderpad=1,
                title='Proportional Fees')
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.title(title + "\n" + subtitle, fontsize=20)
    plt.savefig(fname=os.path.join(plot_path, name + '.png'))
    tikz.save(os.path.join(plot_path, name + '.tex'), encoding='utf-8')
    if plot:
        plt.show()

    plt.close('all')


def plot_freq(df: pd.DataFrame, plot_path, title, name, labels, subtitle, plot=False):
    """

    :param df:
    :param plot_path:
    :param title:
    :param name:
    :param labels:
    :param plot:
    :return:
    """
    df_columns: List[pd.DataFrame] = [df[[column]] for column in df]
    fig, axes = plt.subplots(2, 3, figsize=(20, 10), dpi=100)
    palette = itertools.cycle(sns.color_palette())
    fig.suptitle(title + "\n" + subtitle)
    for df_column, axis in zip(df_columns, axes.flatten()):
        axis.set_xlabel('relay balance in sat')
        axis.set_ylabel('freq')
        sns.distplot(df_column, color=next(palette), ax=axis, kde=False,
                     hist_kws={"rwidth": 0.75, 'edgecolor': 'black', 'alpha': 1.0})
    fig.legend(title='proportional fee:', labels=[str(label_name) for label_name in df.columns],
               loc="upper left", frameon=True, framealpha=0.7, ncol=1, shadow=False, borderpad=1)
    plt.savefig(fname=os.path.join(plot_path, name + '.png'))
    tikz.save(os.path.join(plot_path, name + '.tex'), encoding='utf-8')
    if plot:
        plt.show()
    plt.close('all')

