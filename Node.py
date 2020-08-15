import LightningNetwork
from Channel import Channel


class Node:
    def __init__(self):
        self.channels = dict()
        self.balance = 0

    def create_channel(self, owner_balance, node, node_balance):
        self.channels[node] = Channel(self, owner_balance, node, node_balance)
        self.balance -= LightningNetwork.CHANNEL_COST

    def has_channel(self, node):
        return node in self.channels.keys()

    def transact(self, target, value):
        channel = self.channels[target]
        channel.transact(self, value)



