from enum import Enum
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict
import os


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
        return "r2r {} r2c {} base-fee {} proportional-fee {}".format(self.r2r_balance, self.r2c_balance,
                                                                      self.base_fee, self.proportional_fee)


def store_results(results: Dict[SimulationConfiguration, List[float]], filepath, filename) -> pd.DataFrame:
    """

    :param filepath:
    :param results:
    :param filename:
    :return:
    """
    df = pd.DataFrame.from_dict(results)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    df.to_csv(os.path.join(filepath, filename + '.csv'), index=False)
    return df


def plot_graphs(dfs, plot_path, titles=None):
    """

    :param plot_path:
    :param dfs:
    :param titles:
    :return:
    """
    if type(dfs) is not list:
        dfs = [dfs]
    if titles is None:
        titles = [str(i) for i in range(len(dfs))]
    if type(titles) is not list:
        titles = [titles]
    for df, title in zip(dfs, titles):
        df.plot(title=title, figsize=(20, 10)).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
        plt.savefig(fname=os.path.join(plot_path, title + '.png'))
        plt.show()