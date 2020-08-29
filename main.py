import LiqudityNotAssumed
from datetime import datetime

if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Starting plotting test graphs at " + str(current_time))
    LiqudityNotAssumed.run_simulations_and_plot_graphs(transactions_num=5*10**2,
                                                       avg_across_count=2,
                                                       plot=False)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Starting plotting graphs at " + str(current_time))
    LiqudityNotAssumed.run_simulations_and_plot_graphs(transactions_num=10**5,
                                                       avg_across_count=2,
                                                       plot=False)
