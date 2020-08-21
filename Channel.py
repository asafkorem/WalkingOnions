class Channel:
    def __init__(
            self,
            node1,
            balance1: float,
            node2,
            balance2: float,
            network_configuration
    ):
        """

        :param node1:
        :param balance1:
        :param node2:
        :param balance2:
        :param network_configuration:
        """
        node1.balance -= (balance1 + network_configuration.channel_cost)
        node2.balance -= balance2

        self.node1 = node1
        self.balance1: float = balance1
        self.node2 = node2
        self.balance2: float = balance2

    def transact(self, sender_node, value: float):
        """

        :param sender_node:
        :param value:
        :return:
        """
        if sender_node == self.node1:
            self.balance1 -= value
            self.balance2 += value
            return

        self.balance2 -= value
        self.balance1 += value
