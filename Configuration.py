from typing import List

CHANNEL_COST: float = 44 * (10 ** 3)
HOPS_NUMBER: int = 3
NUMBER_OF_RELAYS: int = 50
NUMBER_OF_CLIENTS: int = 5000
NUMBER_OF_RELAYS_PER_CLIENT: int = 1
R2R_CHANNEL_BALANCES: List[float] = [10 ** 6, 5 * (10 ** 6), 10 ** 7, 10 ** 8]
R2C_CHANNEL_BALANCES: List[float] = [10 ** 6, 5 * (10 ** 6), 10 ** 7, 10 ** 8]
TRANSACTION_PROPORTIONAL_FEES: List[float] = [0.005, 0.01, 0.02, 0.03, 0.04, 0.05]

TRANSACTION_NUM: int = 10 ** 4
AVG_ACROSS_COUNT: int = 5

CPU_NUM_RATIO: float = 0.75
