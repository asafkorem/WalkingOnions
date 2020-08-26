import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict
import os


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

    for df, ylabel, title, name in zip(dfs, ylabels, titles, plot_names):
        df.plot(title=title, figsize=(20, 10))\
            .legend(loc="upper left", frameon=True, framealpha=0.7, ncol=1, shadow=False, borderpad=1,
                    title='Proportional Fees')
        plt.ylabel(ylabel)
        plt.xlabel('Transactions')
        plt.savefig(fname=os.path.join(plot_path, name + '.png'))
        if plot:
            plt.show()


def plot_histogram(df: pd.DataFrame, plot_path, title, plot=False):
    """

    :param plot:
    :param title:
    :param df:
    :param plot_path:
    :return:
    """
    for column in df:
        df[[column]].plot.bar(title=title)
        plt.savefig(fname=os.path.join(plot_path, title + '.png'))
        if plot:
            plt.show()
    plt.close('all')

