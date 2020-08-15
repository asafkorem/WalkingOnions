import LightningNetwork

class Channel:
    def __init__(self, node1, balance1, node2, balance2):
        self.node1 = node1
        self.balance1 = balance1
        self.node2 = node2
        self.balance2 = balance2

    def transact(self, sender_node, value, fee):
        new_value = value - fee

        if sender_node == self.node1:
            self.balance1 += fee
            self.node1 -= new_value
            self.node2 += new_value
            return

        self.balance2 += fee
        self.node2 -= new_value
        self.node1 += new_value
