from Node import Node
from LightningNetwork import LightningNetworkConfiguration


class Channel:
    def __init__(
            self,
            node1: Node,
            balance1: float,
            node2: Node,
            balance2: float,
            network_configuration: LightningNetworkConfiguration
    ):
        """

        :param node1:
        :param balance1:
        :param node2:
        :param balance2:
        :param network_configuration:
        """
        node1.balance -= (balance1 + network_configuration.channel_creation_fee)
        node2.balance -= balance2

        self.node1: Node = node1
        self.balance1: float = balance1
        self.node2: Node = node2
        self.balance2: float = balance2

    def transact(self, sender_node: Node, value: float):
        """

        :param sender_node:
        :param value:
        :return:
        """
        if sender_node == self.node1:
            self.node1 -= value
            self.node2 += value
            return

        self.node2 -= value
        self.node1 += value
