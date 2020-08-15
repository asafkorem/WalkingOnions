import LightningNetwork

class Channel:
    def __init__(self, node1, balance1, node2, balance2):
        node1.balance -= (balance1 + LightningNetwork.CHANNEL_CREATION_FEE)
        node2.balance -= balance2

        self.node1 = node1
        self.balance1 = balance1
        self.node2 = node2
        self.balance2 = balance2

    def transact(self, sender_node, value):
        if sender_node == self.node1:
            self.node1 -= value
            self.node2 += value
            return

        self.node2 -= value
        self.node1 += value
