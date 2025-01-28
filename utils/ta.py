from utils.config import COMMON_CONFIG
from utils.backtest import convert_data_to_bt_format, run_backtest

import pandas_ta as ta
import itertools

def enrich_with_ta(_data, _params):
    """
    Обогащение данных значениями технического анализа

    :param data: DataFrame с данными, на которые будут наложены индикаторы.
    :param params: словарь с параметрами.
    :return: DataFrame с рассчитанными индикаторами и сигналами.
    """
    _df = _data.copy()
    # Извлекаем параметры из словаря
    RSI_period = _params['RSI_period']
    fastMACD_period = _params['fastMACD_period']
    slowMACD_period = _params['slowMACD_period']
    signalMACD_period = _params['signalMACD_period']

    # Добавляем индикаторы
    _close = _df['close']
    _macd_df = ta.macd(_close, fast=fastMACD_period, slow=slowMACD_period, signal=signalMACD_period, talib=False)
    _macd_df.columns = ['macd', 'macd_hist', 'macd_signal']
    _df['macd'] = _macd_df['macd']
    _df['macd_signal'] = _macd_df['macd_signal']
    _df['macd_hist'] = _macd_df['macd_hist']
    _df['RSI'] = ta.rsi(_close, timeperiod=RSI_period, talib=False)
    return _df, ['RSI', 'macd', 'macd_signal', 'macd_hist']

def get_trade_signals(_data, overbought_threshold=70, oversold_threshold=40):
    _df = _data.copy()

    # Создаем сигналы для покупки и продажи
    _df['signal'] = 0

    _df['previous_macd'] = _df['macd'].shift(1)
    _df['previous_macd_signal'] = _df['macd_signal'].shift(1)

    _df.loc[(_df['RSI'] < oversold_threshold)
            & (_df['previous_macd'] < _df['previous_macd_signal'])
            & (_df['macd'] > _df['macd_signal']), 'signal'] = 1  # Сигнал на покупку

    _df.loc[(_df['RSI'] > overbought_threshold)
            & (_df['previous_macd'] > _df['previous_macd_signal'])
            & (_df['macd'] < _df['macd_signal']), 'signal'] = -1  # Сигнал на продажу
    return _df[["date", "open", "high", "low", "close", "volume", "signal"]]

def get_best_params(_data, _strategy, _max_stat_param):
    # Задаем возможные значения для параметров
    RSI_period = [14, 28, 56]
    fastMACD_period_list = [6, 9, 12, 14]
    slowMACD_period_list = [19, 26, 30, 39]
    signalMACD_period_list = [4, 7, 9]

    # Для хранения лучших параметров и лучшего результата
    best_params = None
    best_performance = -float('inf')

    # Проходим по всем комбинациям параметров

    for RSI_period, fastMACD_period, slowMACD_period, signalMACD_period in itertools.product(RSI_period,
                                                                                             fastMACD_period_list,
                                                                                             slowMACD_period_list,
                                                                                             signalMACD_period_list):

        # Создаем словарь с текущими параметрами
        params = {
            'RSI_period': RSI_period,
            'fastMACD_period': fastMACD_period,
            'slowMACD_period': slowMACD_period,
            'signalMACD_period': signalMACD_period
        }

        _ta_data, _ = enrich_with_ta(_data, params)
        _data_with_signals = get_trade_signals(_ta_data)
        _bt_data = convert_data_to_bt_format(_data_with_signals)

        print(f"Выполняем backtesting для параметров {params}")
        _stats = run_backtest(_bt_data, _strategy, plot=False, print_stats=False)

        # Определяем метрику, по которой будем выбирать лучшую стратегию
        performance = _stats[_max_stat_param]
        print(f"Получен результат {performance}")

        # Сравниваем с лучшим результатом и сохраняем лучшие параметры
        if performance > best_performance:
            best_performance = performance
            best_params = params

    print(f"Лучший параметр статистики {_max_stat_param}: {best_performance}")
    print(f"Лучшие параметры технического анализа: {best_params}")
    return best_params