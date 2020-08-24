from LightningNetwork import LightningNetworkConfiguration
from LightningNetwork import LightningNetwork
from typing import Tuple, List
import random
import numpy as np


def is_error_smaller_than_epsilon(epsilon: float = 0.0001):
    """

    :return:
    """
    configuration: LightningNetworkConfiguration = LightningNetworkConfiguration(
        default_balance_client_relay_channel_client=0,
        default_balance_client_relay_channel_relay=0,
        default_balance_relay_relay_channel=0,
        channel_cost=1,
        relay_transaction_fee=100,
        transaction_proportional_fee=0,
        hops_number=3,
        is_liquidity_assumed=True,
        number_of_relays=100,
        number_of_clients=10000,
        number_of_relays_per_client=1
    )

    error: float = calculate_error(
        network_configuration=configuration,
        transactions_count=1000,
        transaction_value_range=(1., 2.)
    )

    return error < epsilon


def calculate_error(network_configuration: LightningNetworkConfiguration, transactions_count: int,
                    transaction_value_range: Tuple[float, float]):
    """

    :param network_configuration:
    :param transactions_count:
    :param transaction_value_range:
    :return:
    """
    lightning_network: LightningNetwork = LightningNetwork(network_configuration)

    expected_relay_balances: List[float] = expected_relay_balance(network_configuration, transactions_count)

    initial_balances = lightning_network.get_relays_balances()
    initial_mean_balance = float(np.mean(initial_balances, dtype=np.float64))
    mean_relay_balances: List[float] = [0] * (transactions_count + 1)
    mean_relay_balances[0] = initial_mean_balance

    for i in range(1, transactions_count + 1):
        c1, c2 = random.sample(lightning_network.clients, 2)
        value = random.uniform(transaction_value_range[0], transaction_value_range[1])
        lightning_network.transact(c1, c2, value)

        balances = lightning_network.get_relays_balances()
        mean_balance = np.mean(balances, dtype=np.float64)
        mean_relay_balances[i] = float(mean_balance)

    errors = [abs(expected_relay_balances[j] - mean_relay_balances[j]) for j in range(len(expected_relay_balances))]
    return float(np.mean(errors))


def expected_relay_balance(network_configuration: LightningNetworkConfiguration, transactions_count: int)\
        -> List[float]:
    """
    Compute the expected relay balance with the analytic equation.
    :param network_configuration:
    :param transactions_count:
    :return:
    """
    tx_fee = network_configuration.relay_transaction_fee
    hops = network_configuration.hops_number
    relays = network_configuration.number_of_relays
    channel_cost = network_configuration.channel_cost
    return [(tx_num * tx_fee * (hops + 2)) * (1 / relays) - channel_cost * (relays - 1) / 2
            for tx_num in range(transactions_count + 1)]
