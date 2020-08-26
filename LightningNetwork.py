from typing import List, Set, Dict, Tuple
from Node import Node
from Client import Client
from Relay import Relay
import random


class LightningNetworkConfiguration:
    def __init__(self,
                 default_balance_client_relay_channel_client: float,
                 default_balance_client_relay_channel_relay: float,
                 default_balance_relay_relay_channel: float,
                 channel_cost: float,
                 relay_transaction_fee: float,
                 transaction_proportional_fee: float,
                 hops_number: int,
                 is_liquidity_assumed: bool,
                 number_of_relays: int,
                 number_of_clients: int,
                 number_of_relays_per_client: int):
        """

        :param default_balance_client_relay_channel_client:
        :param default_balance_client_relay_channel_relay:
        :param default_balance_relay_relay_channel:
        :param channel_cost:
        :param relay_transaction_fee:
        :param transaction_proportional_fee:
        :param hops_number:
        :param is_liquidity_assumed:
        :param number_of_relays:
        :param number_of_clients:
        :param number_of_relays_per_client:
        """
        self.default_balance_client_relay_channel_client: float = default_balance_client_relay_channel_client
        self.default_balance_client_relay_channel_relay: float = default_balance_client_relay_channel_relay
        self.default_balance_relay_relay_channel = default_balance_relay_relay_channel
        self.channel_cost: float = channel_cost
        self.relay_transaction_fee: float = relay_transaction_fee
        self.transaction_proportional_fee: float = transaction_proportional_fee
        self.hops_number: int = hops_number
        self.is_liquidity_assumed: bool = is_liquidity_assumed
        self.number_of_relays: int = number_of_relays
        self.number_of_clients: int = number_of_clients
        self.number_of_relays_per_client: int = number_of_relays_per_client


class LightningNetwork:
    def __init__(self, configuration: LightningNetworkConfiguration):
        """

        :param configuration:
        """
        self.configuration: LightningNetworkConfiguration = configuration
        self.relays: Set[Relay] = self.create_relays()
        self.clients: Set[Client] = self.create_clients()
        self.sum_relays_balances: float = -self.calc_construction_price()

    def create_relays(self) -> Set[Relay]:
        """
        :return: Full-graph of Relays.
        """
        relays: Set[Relay] = set()
        for _ in range(self.configuration.number_of_relays):
            new_relay = Relay(self.configuration)
            for other_relay in relays:
                new_relay.create_channel(
                    self.configuration.default_balance_relay_relay_channel,
                    other_relay,
                    self.configuration.default_balance_relay_relay_channel
                )
            relays.add(new_relay)
        return relays

    def create_clients(self) -> Set[Client]:
        """
        :return: Set of network clients, based on the network configuration, connected to bootstrap relays with
         channels.
        """
        clients: Set[Client] = set()
        for _ in range(self.configuration.number_of_clients):
            bootstrap_relays = random.sample(self.relays, self.configuration.number_of_relays_per_client)
            new_client = Client(bootstrap_relays, self.configuration)
            clients.add(new_client)
        return clients

    def transact(self, source_client: Client, target_client: Client, value: float) -> bool:
        """

        :param source_client:
        :param target_client:
        :param value:
        :return:
        """
        value = self.calculate_value_with_cumulative_fees(value)
        path: List[Node] = self.find_path(source_client, target_client)
        if not self.verify_path(path, value):
            return False

        fees: float = 0
        for i in range(0, len(path) - 1):
            current_node, next_node = path[i], path[i + 1]
            try:
                current_node.transact(next_node, value)
            except Exception:
                raise Exception("Failed to transact between node {0} and node {1} in the path".format(i, i + 1))

            # Deduct the fees from value for the next hop transaction
            value, fees = self.deduct_fees_from_value(value)
            self.sum_relays_balances += fees

        # The fees added to self.fees_collected in the last iteration of the loop above shouldn't be collected.
        self.sum_relays_balances -= fees

        return True

    def calculate_value_with_cumulative_fees(self, value: float) -> float:
        """

        :param value:
        :return:
        """
        return value + self.calculate_cumulative_base_fee() + self.calculate_cumulative_proportional_fee(value)

    def calculate_cumulative_base_fee(self) -> float:
        """

        :return:
        """
        return self.configuration.relay_transaction_fee * (self.configuration.hops_number + 2)

    def calculate_cumulative_proportional_fee(self, value: float) -> float:
        """

        :param value:
        :return:
        """
        num_relays_in_path: int = self.configuration.hops_number + 2
        new_value: float = value / ((1 - self.configuration.transaction_proportional_fee) ** num_relays_in_path)
        return new_value - value

    def deduct_fees_from_value(self, value) -> Tuple[float, float]:
        """

        :param value:
        :return:
        """
        proportional_fee = self.configuration.transaction_proportional_fee * value
        fees = self.configuration.relay_transaction_fee + proportional_fee
        return value - fees, fees

    def find_path(self, source_client: Client, target_client: Client) -> List[Node]:
        """

        :param source_client:
        :param target_client:
        :return:
        """
        first_relay = random.sample(source_client.relays, 1)
        target_relay = random.sample(target_client.relays, 1)

        middle_relays = random.sample(self.relays - set(first_relay + target_relay), self.configuration.hops_number)
        return [source_client] + first_relay + middle_relays + target_relay + [target_client]

    def verify_path(self, path: List[Node], value: float) -> bool:
        """

        :param value:
        :param path:
        :return:
        """
        if value < 0:
            raise ValueError("Tried to send negative value: ", value)

        if self.configuration.is_liquidity_assumed:
            return True

        for i in range(0, len(path) - 1):
            current_node, next_node = path[i], path[i + 1]
            channel = current_node.channels[next_node]

            current_node_balance_in_channel = channel.balance1 if channel.node1 == current_node else channel.balance2
            if value > current_node_balance_in_channel:
                return False

            # Deduct the fees from value for the next hop transaction
            value, fees = self.deduct_fees_from_value(value)

        return True

    # TODO: remove this func
    def get_relays_balances(self) -> List[float]:
        """

        :return:
        """
        relay_to_funds: Dict[Relay, float] = dict()
        for relay in self.relays:
            relay_to_funds[relay] = relay.balance
            for channel in relay.channels.values():
                balance_in_channel = channel.balance1 if channel.node1 == relay else channel.balance2
                relay_to_funds[relay] += balance_in_channel

        return list(relay_to_funds.values())

    def get_relays_mean_balance(self) -> float:
        """
        :return: Returns the mean profit of the relays from transaction fees.
        """
        return self.sum_relays_balances / len(self.relays)

    def calc_construction_price(self) -> float:
        """

        :return:
        """
        return (len(self.relays) - 1) * len(self.relays) * self.configuration.channel_cost / 2
