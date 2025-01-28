import pandas as pd
from backtesting import Backtest
from utils.config import COMMON_CONFIG

def run_backtest(_test_data, _strategy, plot=True, print_stats=True):
    bt = Backtest(_test_data, _strategy, cash=COMMON_CONFIG.CASH, commission=COMMON_CONFIG.COMMISSION)
    stats = bt.run()

    if plot:
        bt.plot()

    if print_stats:
        print(stats)
    return stats

def convert_data_to_bt_format(_data):
    _df = _data.copy()
    _df.columns = _df.columns.str.capitalize()
    _df.rename(columns={'Date': 'Datetime'}, inplace=True)
    _df["Datetime"] = pd.to_datetime(_df["Datetime"])
    _df.set_index('Datetime', inplace=True)
    return _df