from Node import Node
from Channel import Channel
import LightningNetwork


class Client(Node):
    def __init__(self, bootstrap_relays):
        super().__init__()
        self.relays = bootstrap_relays
        for relay in bootstrap_relays:
            self.create_channel_with_relay(relay)

    def create_channel_with_relay(self, relay):
        self.channels[relay] = self.create_channel(LightningNetwork.DEFAULT_LIQUIDITY_CLIENT_RELAY_CHANNEL_OWNER,
                                                   relay, LightningNetwork.DEFAULT_LIQUIDITY_CLIENT_RELAY_CHANNEL_RELAY)


