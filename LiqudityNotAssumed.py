from LightningNetwork import LightningNetworkConfiguration
from LightningNetwork import LightningNetwork
from typing import Tuple, List, Dict
from LogNormal import LogNormal
import random
import numpy as np
from itertools import product
from enum import Enum
import matplotlib.pyplot as plt


def plot_graphs():
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

    class FeeType(Enum):
        BASE = 0
        PROPORTIONAL = 0

    transaction_fee_types = [FeeType.BASE, FeeType.PROPORTIONAL]

    # Dictionary keys order: r2r_balance, r2c_balance, fee_type.
    configuration_to_avg_mean_balances: Dict[Tuple[float, float, FeeType], List[float]] = dict()
    configuration_to_avg_fail_rates: Dict[Tuple[float, float, FeeType], List[float]] = dict()

    for r2r_balance, r2c_balance, fee_type \
            in product(r2r_channel_balances, r2c_channel_balances, transaction_fee_types):
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
        avg_across_count = 5

        mean_balances_results: List[List[float]] = list()
        fail_rates_results: List[List[float]] = list()
        for i in range(avg_across_count):
            transactions_num = 10 ** 4
            transactions_values = LogNormal(size=transactions_num).get_samples()

            mean_balances, fail_rates = calculate_mean_balances_and_fail_rates(
                network_configuration=network_configuration,
                transaction_values=transactions_values
            )

            mean_balances_results.append(mean_balances)
            fail_rates_results.append(fail_rates)

        avg_mean_balances: List[float] = [sum(elements) / avg_across_count for elements in zip(*mean_balances_results)]
        avg_fail_rates: List[float] = [sum(elements) / avg_across_count for elements in zip(*fail_rates_results)]

        configuration: Tuple[float, float, FeeType] = Tuple[r2r_balance, r2c_balance, fee_type]
        configuration_to_avg_mean_balances[configuration] = avg_mean_balances
        configuration_to_avg_fail_rates[configuration] = avg_fail_rates

    # TODO: Plot graphs by fee type:
    for r2r_balance, r2c_balance in product(r2r_channel_balances, r2c_channel_balances):
        configuration_name: str = \
            "R2R initial balance: {}, R2C initial balance (relay): {}".format(r2r_balance, r2c_balance)


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

    initial_balances = lightning_network.get_relays_balances()
    initial_mean_balance = float(np.mean(initial_balances, dtype=np.float64))

    mean_balances: List[float] = [0] * (len(transaction_values) + 1)
    mean_balances[0] = initial_mean_balance

    num_fails = 0
    fail_rates: List[float] = [0] * (len(transaction_values) + 1)

    # Make index start with 1
    for i, value in enumerate(transaction_values, 1):
        c1, c2 = random.sample(lightning_network.clients, 2)

        if not lightning_network.transact(c1, c2, value):
            num_fails += 1
        fail_rates[i] = num_fails / i

        balances = lightning_network.get_relays_balances()
        mean_balance = np.mean(balances, dtype=np.float64)
        mean_balances[i] = float(mean_balance)

    return mean_balances, fail_rates
