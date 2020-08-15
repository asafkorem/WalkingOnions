from typing import List
from Node import Node

CHANNEL_COST = 5
NODE_DEFAULT_BALANCE = 0
CHANNEL_OWNERS_DEFAULT_BALANCE = 0
RELAY_TRANSACTION_FEE = 1


class LightningNetwork:
    def __init__(self):
        pass

    def  transact(self, c1, c2, value):
        path = self.choose_path(c1, c2)
        for i in range(len(path) - 1):
            path[i].transact(path[i + 1], value - i * RELAY_TRANSACTION_FEE)

    def choose_path(self, c1, c2) -> list[Node]:
