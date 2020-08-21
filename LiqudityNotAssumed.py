from LightningNetwork import LightningNetworkConfiguration
from LightningNetwork import LightningNetwork
from typing import Tuple, List
import random
import numpy as np
import matplotlib.pyplot as plt
from LightningNetwork import FAIL_INDEX_HISTOGRAM


def plot_relays_mean_balances():
    """

    :return:
    """
    configuration: LightningNetworkConfiguration = LightningNetworkConfiguration(
        default_balance_client_relay_channel_client=float('inf'),
        default_balance_client_relay_channel_relay=20,
        default_balance_relay_relay_channel=20,
        channel_cost=1,
        relay_transaction_fee=0.1,
        hops_number=3,
        is_liquidity_assumed=False,
        number_of_relays=100,
        number_of_clients=10000,
        number_of_relays_per_client=5
    )

    relays_mean_balances, num_failed_ratio_array = calculate_relays_mean_balances(configuration, 10**4, (1., 10.))

    plt.title("No Liquidity Assumption Relays Mean Balances")
    plt.plot(range(len(relays_mean_balances)), relays_mean_balances)
    plt.show()

    plt.title("No Liquidity Assumption Num Fails")
    plt.plot(range(len(num_failed_ratio_array)), num_failed_ratio_array)
    plt.show()

    plt.title("No Liquidity Assumption Relays Mean Balances Derivative")
    dx = 1
    dy = np.diff(relays_mean_balances) / dx
    plt.plot(range(len(dy)), dy)
    plt.show()


def calculate_relays_mean_balances(network_configuration: LightningNetworkConfiguration, transactions_count: int,
                                   transaction_value_range: Tuple[float, float]):
    """

    :param network_configuration:
    :param transactions_count:
    :param transaction_value_range:
    :return:
    """
    lightning_network: LightningNetwork = LightningNetwork(network_configuration)
    initial_balances = lightning_network.get_relays_balances()
    initial_mean_balance = float(np.mean(initial_balances, dtype=np.float64))
    relays_mean_balances: List[float] = [initial_mean_balance] * (transactions_count + 1)
    num_fails = 0
    num_fails_ratio_array = [0.0] * (transactions_count + 1)

    for i in range(transactions_count):
        c1, c2 = random.sample(lightning_network.clients, 2)
        value = random.uniform(transaction_value_range[0], transaction_value_range[1])
        transaction_succeeded = lightning_network.transact(c1, c2, value)
        if not transaction_succeeded:
            num_fails += 1
        fail_ratio = num_fails / (i + 1)
        num_fails_ratio_array[i + 1] = fail_ratio
        balances = lightning_network.get_relays_balances()
        mean_balance = np.mean(balances, dtype=np.float64)
        relays_mean_balances[i + 1] = float(mean_balance)
        if i % 100 == 0:
            print('iteration num: ' + str(i) + ' transaction succeded: ' + str(transaction_succeeded) +
                  ', mean balance: ' + str(mean_balance) + ', fail ratio: ' + str(fail_ratio) + ', fail histogram: '
                  + str(FAIL_INDEX_HISTOGRAM))
    print(FAIL_INDEX_HISTOGRAM)

    return relays_mean_balances, num_fails_ratio_array
