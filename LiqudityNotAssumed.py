from LightningNetwork import LightningNetworkConfiguration
from LightningNetwork import LightningNetwork
from typing import Tuple, List, Dict, Optional
from LogNormal import LogNormal
import random
import numpy as np
from itertools import product
from enum import Enum
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


class FeeType(Enum):
    BASE = 0
    PROPORTIONAL = 1


class SimulationConfiguration:
    def __init__(self, r2r_balance, r2c_balance, fee_type):
        self.r2r_balance = r2r_balance
        self.r2c_balance = r2c_balance
        self.fee_type = fee_type

    def __hash__(self):
        return hash((self.r2c_balance, self.r2c_balance, self.fee_type))

    def __eq__(self, other):
        return (self.r2c_balance, self.r2c_balance, self.fee_type)\
               == (other.r2c_balance, other.r2c_balance, other.fee_type)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __str__(self):
        return "r2r {} r2c {} fee_type {}".format(self.r2r_balance, self.r2c_balance,
                                                  "base_fee" if self.fee_type == FeeType.BASE else "proportional_fee")


def run_simulations_and_plot_graphs(transactions_num=10**4, avg_across_count=5):
    """
    Plot graphs, for each transaction fee (base fee = 100 and proportional_fee = 1%).
    For each graph, show the Relay expected balance and fail ratio.
    """
    channel_cost = 44 * (10 ** 3)   # Based on avg. miners fee
    hops_number = 3
    number_of_relays = 10 ** 3
    number_of_clients = 10 ** 5
    number_of_relays_per_client = 1

    # 0.5M, 10M and 100M Satoshies.
    r2r_channel_balances: List[float] = [5 * (10 ** 6), 10 ** 7, 10 ** 8]
    r2c_channel_balances: List[float] = [5 * (10 ** 6), 10 ** 7, 10 ** 8]

    transaction_base_fee = 100
    transaction_proportional_fee = 0.01

    transaction_fee_types = [FeeType.BASE, FeeType.PROPORTIONAL]

    configuration_to_avg_mean_balances: Dict[SimulationConfiguration, List[float]] = dict()
    configuration_to_avg_fail_rates: Dict[SimulationConfiguration, List[float]] = dict()

    for r2r_balance, r2c_balance, fee_type \
            in product(r2r_channel_balances, r2c_channel_balances, transaction_fee_types):
        print("Running simulation for the following configuration:\nr2r_balance=%s, r2c_balance=%s, fee_type=%s" %
              (str(r2r_balance), str(r2c_balance), "base_fee" if fee_type == FeeType.BASE else "proportional_fee"))
        network_configuration = LightningNetworkConfiguration(
            default_balance_client_relay_channel_client=float('inf'),
            default_balance_client_relay_channel_relay=r2c_balance,
            default_balance_relay_relay_channel=r2r_balance,
            channel_cost=channel_cost,
            relay_transaction_fee=transaction_base_fee if fee_type == FeeType.BASE else 0,
            transaction_proportional_fee=transaction_proportional_fee if fee_type == FeeType.PROPORTIONAL else 0,
            hops_number=hops_number,
            is_liquidity_assumed=True,
            number_of_relays=number_of_relays,
            number_of_clients=number_of_clients,
            number_of_relays_per_client=number_of_relays_per_client
        )

        # Change this value to avg across more values:

        mean_balances_results: List[List[float]] = list()
        fail_rates_results: List[List[float]] = list()
        for i in range(avg_across_count):
            print("iter %s out of %s" % (str(i + 1), str(avg_across_count)))
            transactions_values = LogNormal(size=transactions_num).get_samples()

            mean_balances, fail_rates = calculate_mean_balances_and_fail_rates(
                network_configuration=network_configuration,
                transaction_values=transactions_values
            )

            mean_balances_results.append(mean_balances)
            fail_rates_results.append(fail_rates)

        avg_mean_balances: List[float] = [sum(elements) / avg_across_count for elements in zip(*mean_balances_results)]
        avg_fail_rates: List[float] = [sum(elements) / avg_across_count for elements in zip(*fail_rates_results)]

        configuration: SimulationConfiguration = SimulationConfiguration(r2r_balance, r2c_balance, fee_type)
        configuration_to_avg_mean_balances[configuration] = avg_mean_balances
        configuration_to_avg_fail_rates[configuration] = avg_fail_rates

    avg_mean_balances_df = store_results(configuration_to_avg_mean_balances, "Avg Relay Mean Balances in Satoshi")
    fail_ratio_df = store_results(configuration_to_avg_fail_rates, "Fail Ratio")
    plot_graphs([avg_mean_balances_df, fail_ratio_df], ["Avg Relay Mean Balances in Satoshi", "Fail Ratio"])


def calculate_mean_balances_and_fail_rates(
        network_configuration: LightningNetworkConfiguration,
        transaction_values: List[float]
) -> (List[float], List[float]):
    """

    :param network_configuration:
    :param transaction_values:
    :return:
    """
    lightning_network: LightningNetwork = LightningNetwork(network_configuration)
    initial_mean_balance = lightning_network.get_relays_mean_balance()

    mean_balances: List[float] = [0] * (len(transaction_values) + 1)
    mean_balances[0] = initial_mean_balance

    num_fails = 0
    fail_rates: List[float] = [0] * (len(transaction_values) + 1)

    # Make index start with 1
    for i, value in enumerate(transaction_values, 1):
        # print("transaction %s out of %s" % (str(i), str(len(transaction_values))))
        c1, c2 = random.sample(lightning_network.clients, 2)

        if not lightning_network.transact(c1, c2, value):
            num_fails += 1
        fail_rates[i] = num_fails / i
        mean_balances[i] = lightning_network.get_relays_mean_balance()

    return mean_balances, fail_rates


def store_results(results: Dict[SimulationConfiguration, List[float]], plot_name) -> pd.DataFrame:
    """

    :param results:
    :param plot_name:
    :return:
    """
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H-%M-%S")
    df = pd.DataFrame.from_dict(results)
    directory = os.path.join("results", current_date_time)
    if not os.path.exists(directory):
        os.mkdir(directory)
    df.to_csv(os.path.join("results", current_date_time, plot_name + '.csv'), index=False)
    return df


def plot_graphs(dfs, titles: Optional[List[str]] = None):
    """

    :param dfs:
    :param titles:
    :return:
    """
    if type(dfs) is not list:
        dfs = [dfs]
    if titles is None:
        titles = [str(i) for i in range(len(dfs))]
    for df, title in zip(dfs, titles):
        df.plot(title=title)
        plt.show()
