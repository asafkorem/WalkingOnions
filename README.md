# Walking Onions Simulator For Lightning Network:
Simulator for evaluating the application of Walking Onions protocol on Lightning Network.

## How to run the simulator:
To run the simulator, run the file main.py.

## Editing Network configurations:
In order to customize the configuration of the network, edit the file Configuration.py
The parameters that can be edited are:

CHANNEL_COST: The cost of the payment channel on the network (miner fee) in satoshi. (CONSTANT)
HOPS_NUMBER: The number of middle relays in transactions' path. (CONSTANT)
NUMBER_OF_RELAYS: The number of relays in the network. (CONSTANT)
NUMBER_OF_CLIENTS: The number of clients in the network. (CONSTANT)
NUMBER_PER_RELAYS_PER_CLIENT: The number of relays each client is connected to. (CONSTANT)
R2R_CHANNEL_BALANCES: A list of amounts of satoshi relays lock in relay-to-relay channels. (LIST)
R2C_CHANNEL_BALANCES: A list of amounts of satoshi relays lock in channels with clients. (LIST)
TRANSACTION_PROPORTIONAL_FEES: A list of transaction proportional fee ratios relays take for forwarding
 transactions. (LIST)
 
TRANSACTION_NUM: The number of transactions the simulation will perform on each configuration. (CONSTANT)
AVG_ACROSS_COUNT: The number of simulations to perform for each configuration to average results across. (CONSTANT)
CPU_NUM_RATIO: Ratio of available CPU cores that will be used for running the simulator. (CONSTANT)

### Notice:
R2R_CHANNEL_BALANCES, R2C_CHANNEL_BALANCES, TRANSACTION_PROPORTIONAL_FEES are lists.
The number of resulting configurations the simulator will run simulations for is:
len(R2R_CHANNEL_BALANCES) * len(R2C_CHANNEL_BALANCES) * len(TRANSACTION_PROPORTIONAL_FEES)

## Plotting the Results and Storing the Results:

After the simulator finishes running, plots are presented and stored in "results" folder. Together with plots in a png
format, the results are also stored in tex and pickle file formats. 

