from LightningNetwork import LightningNetworkConfiguration
from LightningNetwork import LightningNetwork
from typing import Tuple, List
import random
import numpy as np
import matplotlib.pyplot as plt


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
        number_of_relays=20,
        number_of_clients=10000,
        number_of_relays_per_client=10
    )

    relays_mean_balances, num_failed_ratio_array = calculate_relays_mean_balances(configuration, 10**3, (1, 10))

    plt.title("No Liquidity Assumption Relays Mean Balances")
    plt.plot(range(len(relays_mean_balances)), relays_mean_balances)
    plt.show()

    plt.title("No Liquidity Assumption Failure Ratio")
    plt.plot(range(len(num_failed_ratio_array)), num_failed_ratio_array)
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
    relays_mean_balances: List[float] = [0] * (transactions_count + 1)
    relays_mean_balances[0] = initial_mean_balance
    num_fails = 0
    num_fails_ratio_array: List[float] = [0] * (transactions_count + 1)

    for i in range(1, transactions_count + 1):
        c1, c2 = random.sample(lightning_network.clients, 2)
        value = random.uniform(transaction_value_range[0], transaction_value_range[1])
        transaction_succeeded = lightning_network.transact(c1, c2, value)
        if not transaction_succeeded:
            num_fails += 1
        fail_ratio = num_fails / i
        num_fails_ratio_array[i] = fail_ratio
        balances = lightning_network.get_relays_balances()
        mean_balance = np.mean(balances, dtype=np.float64)
        relays_mean_balances[i] = float(mean_balance)
        if i % 100 == 0:
            print('iteration num: ' + str(i) + ' transaction succeeded: ' + str(transaction_succeeded) +
                  ', mean balance: ' + str(mean_balance) + ', fail ratio: ' + str(fail_ratio))

    # channels = set()
    # for relay in lightning_network.relays:
    #     channels = channels.union(set(relay.channels.values()))
    #
    # l = [(c.balance1, c.balance2) for c in channels]
    #
    # for z in l:
    #     if z[0] == float('inf') or z[1] == float('inf'):
    #         continue
    #
    #     print("values")
    #     print(z[0])
    #     print(z[1])
    #     print()

    return relays_mean_balances, num_fails_ratio_array
