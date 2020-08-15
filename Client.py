from Node import Node
from Relay import Relay
from typing import List
from LightningNetwork import LightningNetworkConfiguration


class Client(Node):
    def __init__(self, bootstrap_relays: List[Relay], network_configuration: LightningNetworkConfiguration):
        super().__init__(network_configuration)
        self.network_configuration: LightningNetworkConfiguration = network_configuration
        self.relays: List[Relay] = bootstrap_relays
        for relay in bootstrap_relays:
            self.create_channel_with_relay(relay)

    def create_channel_with_relay(self, relay: Relay):
        self.create_channel(
            self.network_configuration.default_balance_client_relay_channel_client,
            relay,
            self.network_configuration.default_balance_client_relay_channel_relay
        )


