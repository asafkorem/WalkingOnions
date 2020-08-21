from typing import List, Set, Dict
from Node import Node
from Client import Client
from Channel import Channel
from Relay import Relay
import random


class LightningNetworkConfiguration:
    def __init__(self,
                 default_balance_client_relay_channel_client: float,
                 default_balance_client_relay_channel_relay: float,
                 default_balance_relay_relay_channel: float,
                 channel_cost: float,
                 relay_transaction_fee: float,
                 path_find_max_retries: int,
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
        :param path_find_max_retries:
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
        self.path_find_max_retries: int = path_find_max_retries
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
        self.cancelled_transactions_count: int = 0
        self.total_transactions: int = 0
        self.relays: Set[Relay] = self.create_relays()
        self.clients: Set[Client] = self.create_clients()

    def create_relays(self) -> Set[Relay]:
        """
        :return: Full-graph of Relays.
        """
        relays: Set[Relay] = set()
        for i in range(self.configuration.number_of_relays):
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

        :return:
        """
        clients: Set[Client] = set()
        for i in range(self.configuration.number_of_clients):
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
        path: List[Node] = self.find_path(source_client, target_client)
        if not self.verify_path(path):
            return False

        for i in range(1, len(path)):
            net_value_for_step = value - i * self.configuration.relay_transaction_fee
            try:
                path[i - 1].transact(path[i], net_value_for_step)
            except Exception:
                raise Exception("Failed to transact between node {0} and node {1} in the path".format(i - 1, i))
        return True

    def find_path(self, source_client: Client, target_client: Client) -> List[Node]:
        """

        :param source_client:
        :param target_client:
        :return:
        """
        first_hop = random.sample(source_client.relays, 1)
        target_relay = random.sample(target_client.relays, 1)

        middle_relays = random.sample(self.relays - set(first_hop) - set(target_relay), self.configuration.hops_number)
        return [source_client] + first_hop + middle_relays + target_relay + [target_client]

    def verify_path(self, path: List[Node]) -> bool:
        """

        :param path:
        :return:
        """
        if self.configuration.is_liquidity_assumed:
            return True
        # TODO: else verify whether the path is legal (liquid)

        return False

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


