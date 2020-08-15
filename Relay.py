from LightningNetwork import LightningNetworkConfiguration
from Node import Node


class Relay(Node):
    def __init__(self, network_configuration: LightningNetworkConfiguration):
        """

        :param network_configuration:
        """
        super().__init__(network_configuration)

