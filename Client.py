from Node import Node
from Relay import Relay
from typing import List


class Client(Node):
    def __init__(self, bootstrap_relays: List[Relay], network_configuration):
        """

        :param bootstrap_relays:
        :param network_configuration:
        """
        super().__init__(network_configuration)
        self.network_configuration = network_configuration
        self.relays: List[Relay] = bootstrap_relays
        for relay in bootstrap_relays:
            self.create_channel_with_relay(relay)

    def create_channel_with_relay(self, relay: Relay):
        """

        :param relay:
        :return:
        """
        self.create_channel(
            owner_balance=self.network_configuration.default_balance_client_relay_channel_client,
            other_owner=relay,
            other_owner_balance=self.network_configuration.default_balance_client_relay_channel_relay
        )


