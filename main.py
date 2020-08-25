import LiquidityAssumed
import LiqudityNotAssumed
from datetime import datetime

if __name__ == '__main__':
    # print("INFORMATIVE MESSAGE FOR STEP 1", LiquidityAssumed.is_error_smaller_than_epsilon())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Starting plotting Liquidity Not Assumed graphs at " + str(current_time))
    LiqudityNotAssumed.plot_graphs(transactions_num=10**3, avg_across_count=2)
    

