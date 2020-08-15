import LightningNetwork
from Channel import Channel


class Node:
    def __init__(self):
        self.channels = []
        self.balance = LightningNetwork.NODE_DEFAULT_BALANCE

    def create_channel(self, node):
        default_balance = LightningNetwork.CHANNEL_OWNERS_DEFAULT_BALANCE
        new_channel = Channel(self, default_balance, node, default_balance)
        self.channels.append(new_channel)
        self.balance -= LightningNetwork.CHANNEL_COST

    def transact(self, target, value):
        pass

