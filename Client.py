from Node import Node
import LightningNetwork


class Client(Node):
    def __init__(self, relays):
        self.channels = []
        self.bootsrap_relays = set()

    def transact_in_path(self, path):
        path_started = False
        for node in path:
            if not path_started:
                path_started = True


