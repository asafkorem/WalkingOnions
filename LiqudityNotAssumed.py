from LightningNetwork import LightningNetworkConfiguration
from LightningNetwork import LightningNetwork
from typing import Tuple, List, Dict
from LogNormal import LogNormal
import random
from itertools import product
import os
from datetime import datetime
from multiprocessing import Pool, cpu_count
import tqdm
import istarmap
from statistics import mean
from util import plot_graphs, plot_histogram, store_results, SimulationConfiguration


def run_simulations_and_plot_graphs(transactions_num=10 ** 4, avg_across_count=5, plot=True):
    """
    Plot graphs, for each transaction fee (base fee = 100 and proportional_fee = 1%).
    For each graph, show the Relay expected balance and fail ratio.
    """
    channel_cost = 44 * (10 ** 3)  # Based on avg. miners fee
    hops_number = 3
    number_of_relays = 100
    number_of_clients = 10 ** 5
    number_of_relays_per_client = 1

    # 0.5M, 10M and 100M Satoshies.
    r2r_channel_balances: List[float] = [10 ** 6, 5 * (10 ** 6), 10 ** 7, 10 ** 8]
    r2c_channel_balances: List[float] = [10 ** 6, 5 * (10 ** 6), 10 ** 7, 10 ** 8]

    transaction_proportional_fees = [0.005, 0.01, 0.02, 0.03, 0.04, 0.05]

    # We need to make sure that every configuration is simulated on the same list of transaction values in order to
    # compare between them correctly.
    transaction_samples: List[List[float]] = [LogNormal(size=transactions_num).get_samples()
                                              for _ in range(avg_across_count)]

    configurations = product(r2r_channel_balances, r2c_channel_balances, transaction_proportional_fees)
    groups = [(r2c_balance,
               r2r_balance,
               transaction_proportional_fee,
               channel_cost,
               hops_number,
               number_of_relays,
               number_of_clients,
               number_of_relays_per_client,
               transaction_samples) for r2r_balance, r2c_balance, transaction_proportional_fee in configurations]
    with Pool(cpu_count()) as pool:
        results = list(tqdm.tqdm(pool.istarmap(run_simulation, groups, chunksize=1), total=len(groups)))

    configuration_to_avg_mean_balances: Dict[SimulationConfiguration, List[float]]\
        = {configuration: avg_mean_balances
           for configuration, avg_mean_balances, avg_fail_rates, avg_fail_histogram in results}
    configuration_to_avg_fail_rates: Dict[SimulationConfiguration, List[float]]\
        = {configuration: avg_fail_rates
           for configuration, avg_mean_balances, avg_fail_rates, avg_fail_histogram in results}
    configuration_to_avg_fail_histograms: Dict[SimulationConfiguration, List[float]] =\
        {configuration: avg_fail_histogram
         for configuration, avg_mean_balances, avg_fail_rates, avg_fail_histogram in results}

    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H-%M-%S")
    subdirectory_name = "t_nu-" + str(transactions_num) + " avg_across-" + str(avg_across_count) + " time-" + str(current_date_time)
    plot_path = os.path.join('results', subdirectory_name)

    for r2r, r2c in product(r2r_channel_balances, r2c_channel_balances):
        current_configuration_to_avg_mean_balances = \
            {key:configuration_to_avg_mean_balances[key] for key in configuration_to_avg_mean_balances.keys()
             if key.r2r_balance == r2r and key.r2c_balance == r2c}
        current_configuration_to_avg_fail_rates = \
            {key: configuration_to_avg_fail_rates[key] for key in configuration_to_avg_fail_rates.keys()
             if key.r2r_balance == r2r and key.r2c_balance == r2c}
        current_configuration_to_avg_fail_histogram = \
            {key: configuration_to_avg_fail_histograms[key] for key in configuration_to_avg_fail_histograms.keys()
             if key.r2r_balance == r2r and key.r2c_balance == r2c}

        avg_mean_balances_df = store_results(current_configuration_to_avg_mean_balances, plot_path,
                                             "Avg Relay Mean Balances in Satoshi r2r {} r2c {}".format(r2r, r2c))
        fail_ratio_df = store_results(current_configuration_to_avg_fail_rates, plot_path,
                                      "Fail Ratio r2r {} rtc {}".format(r2r, r2c))
        plot_graphs([avg_mean_balances_df, fail_ratio_df], plot_path,
                    ["Mean Balance", "Fail Rate"],
                    ["Mean Balance of Relays", "Fail Rate"],
                    ["Mean Balance of Relays r2r {} r2c {}".format(r2r, r2c),
                     "Fail Rate r2r {} r2c {}".format(r2r, r2c)], plot=plot)

        avg_fail_histogram_df = store_results(current_configuration_to_avg_fail_histogram, plot_path,
                                              "Transaction Fail Histogram", csv=False)
        plot_histogram(avg_fail_histogram_df, plot_path, "Fail Histogram r2r {} rtc {}".format(r2r, r2c), plot=plot)


def calc_mean_balances_and_fail_rates_fail_histograms(
        network_configuration: LightningNetworkConfiguration,
        transaction_values: List[float]
) -> (List[float], List[float], List[int]):
    """

    :param network_configuration:
    :param transaction_values:
    :return:
    """
    lightning_network: LightningNetwork = LightningNetwork(network_configuration)

    mean_balances: List[float] = [0] * (len(transaction_values) + 1)
    mean_balances[0] = lightning_network.get_relays_mean_balance()

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

    return mean_balances, fail_rates, lightning_network.fail_histogram


def run_simulation(r2c_balance,
                   r2r_balance,
                   transaction_proportional_fee,
                   channel_cost,
                   hops_number,
                   number_of_relays,
                   number_of_clients,
                   number_of_relays_per_client,
                   transaction_samples) -> Tuple[SimulationConfiguration, List[float], List[float], List[float]]:
    """

    :param r2c_balance:
    :param r2r_balance:
    :param transaction_proportional_fee:
    :param channel_cost:
    :param hops_number:
    :param number_of_relays:
    :param number_of_clients:
    :param number_of_relays_per_client:
    :param transaction_samples:
    :return:
    """
    network_configuration = LightningNetworkConfiguration(
        default_balance_client_relay_channel_client=float('inf'),
        default_balance_client_relay_channel_relay=r2c_balance,
        default_balance_relay_relay_channel=r2r_balance,
        channel_cost=channel_cost,
        relay_transaction_fee=0,
        transaction_proportional_fee=transaction_proportional_fee,
        hops_number=hops_number,
        is_liquidity_assumed=False,
        add_fees_to_value=False,
        number_of_relays=number_of_relays,
        number_of_clients=number_of_clients,
        number_of_relays_per_client=number_of_relays_per_client
    )

    mean_balances_results: List[List[float]] = list()
    fail_rates_results: List[List[float]] = list()
    fail_histogram_results: List[List[int]] = list()

    for i, transactions_values in enumerate(transaction_samples, 1):
        mean_balances, fail_rates, fail_histogram = calc_mean_balances_and_fail_rates_fail_histograms(
            network_configuration=network_configuration,
            transaction_values=transactions_values
        )

        mean_balances_results.append(mean_balances)
        fail_rates_results.append(fail_rates)
        fail_histogram_results.append(fail_histogram)

    avg_mean_balances: List[float] = [mean(elements) for elements in zip(*mean_balances_results)]
    avg_fail_rates: List[float] = [mean(elements) for elements in zip(*fail_rates_results)]
    avg_fail_histogram: List[float] = [mean(elements) for elements in zip(*fail_histogram_results)]

    configuration: SimulationConfiguration = SimulationConfiguration(r2r_balance, r2c_balance, 0,
                                                                     transaction_proportional_fee)

    return configuration, avg_mean_balances, avg_fail_rates, avg_fail_histogram
