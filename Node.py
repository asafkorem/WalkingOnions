from __future__ import annotations
from LightningNetwork import LightningNetworkConfiguration
from Channel import Channel
from typing import Dict


class Node:
    def __init__(self, network_configuration: LightningNetworkConfiguration):
        """

        :param network_configuration:
        """
        self.network_configuration: LightningNetworkConfiguration = network_configuration
        self.channels: Dict[Node, Channel] = dict()
        self.balance: float = 0

    def create_channel(self, owner_balance: float, other_owner: Node, other_owner_balance: float):
        """

        :param owner_balance:
        :param other_owner:
        :param other_owner_balance:
        :return:
        """
        if self.has_channel(other_owner):
            raise Exception("Channel with other owner already exists!")

        new_channel = Channel(self, owner_balance, other_owner, other_owner_balance, self.network_configuration)
        self.balance -= (owner_balance + self.network_configuration.channel_cost)
        other_owner.balance -= other_owner_balance

        # Update both nodes with the new channel:
        self.channels[other_owner] = new_channel
        other_owner.channels[self] = new_channel

    def has_channel(self, node: Node):
        """

        :param node:
        :return:
        """
        return node in self.channels.keys()

    def transact(self, target: Node, value: float):
        """

        :param target:
        :param value:
        :return:
        """
        channel: Channel = self.channels[target]
        channel.transact(self, value)



