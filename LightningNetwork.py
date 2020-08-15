from typing import List
from Node import Node
from Client import Client
from Relay import Relay
import random

CHANNEL_COST = 5
DEFAULT_LIQUIDITY_CLIENT_RELAY_CHANNEL_OWNER = float('inf')
DEFAULT_LIQUIDITY_CLIENT_RELAY_CHANNEL_RELAY = 100
CHANNEL_CREATION_FEE = 1
RELAY_TRANSACTION_FEE = 1
PATH_FIND_MAX_RETRY = 10
HOPS_NUMBER = 3


class LightningNetwork:
    def __init__(self, num_relays):
        self.relays = {Relay() for i in range(num_relays)}
        self.cancelled_transactions_count = 0
        self.total_transactions = 0

    def transact(self, c1, c2, value) -> bool:
        path = self.find_path(c1, c2, HOPS_NUMBER)
        if not self.verify_path(path):
            return False

        for i in range(len(path) - 1):
            path[i].transact(path[i + 1], value - (i + 1) * RELAY_TRANSACTION_FEE)
        return True

    def find_path(self, source_node: Client, target_node, hopes_num) -> List[Node]:
        first_hop = random.sample(source_node.relays, 1)
        middle_relays = random.sample(self.relays, hopes_num)
        target_relay = random.sample(target_node.relays, 1)
        return [source_node] + first_hop + middle_relays + target_relay + [target_node]

    def verify_path(self, path) -> bool:
        return False

