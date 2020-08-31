import LiqudityNotAssumed
from datetime import datetime

if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Starting plotting test graphs at " + str(current_time))
    LiqudityNotAssumed.run_simulations_and_plot_graphs()
