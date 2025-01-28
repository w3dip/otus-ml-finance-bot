import pandas as pd
from utils.config import COMMON_CONFIG

def train_test_split(_data):
    # Определяем дату начала тестовой выборки
    _test_start_date = _data.index.max() - pd.DateOffset(months=int(COMMON_CONFIG.TEST_DATA_OFFSET[0]))

    # Разделение данных на тренировочную и тестовую выборки по времени
    _train_data = _data[_data.index < _test_start_date]
    _test_data = _data[_data.index >= _test_start_date]

    print(f"Train size: {len(_train_data)}, Test size: {len(_test_data)}")
    return _train_data, _test_data

def train_test_split_by_date(_data):
    # Определяем дату начала тестовой выборки
    _test_start_date = _data['date'].max() - pd.DateOffset(months=int(COMMON_CONFIG.TEST_DATA_OFFSET[0]))

    # Определяем дату начала валидационной выборки
    _val_start_date = _data['date'].max() - pd.DateOffset(months=COMMON_CONFIG.VAL_DATA_OFFSET[0])

    # Разделение данных на тренировочную, валидационную и тестовую выборки по времени
    _train_data = _data[_data['date'] < _val_start_date]
    _val_data = _data[(_data['date'] >= _val_start_date) & (_data['date'] < _test_start_date)]
    _test_data = _data[_data['date'] >= _test_start_date]

    print(f"Train size: {len(_train_data)}, Val size: {len(_val_data)}, Test size: {len(_test_data)}")
    return _train_data, _val_data, _test_data

# def train_test_split_by_date_with_index(_data):
#     # Определяем дату начала тестовой выборки
#     _test_start_date = _data.index.max() - pd.DateOffset(months=int(COMMON_CONFIG.TEST_DATA_OFFSET[0]))
#
#     # Определяем дату начала валидационной выборки
#     _val_start_date = _data.index.max() - pd.DateOffset(months=COMMON_CONFIG.VAL_DATA_OFFSET[0])
#
#     # Разделение данных на тренировочную, валидационную и тестовую выборки по времени
#     _train_data = _data[_data.index < _val_start_date]
#     _val_data = _data[(_data.index >= _val_start_date) & (_data.index < _test_start_date)]
#     _test_data = _data[_data.index >= _test_start_date]
#
#     print(f"Train size: {len(_train_data)}, Val size: {len(_val_data)}, Test size: {len(_test_data)}")
#     return _train_data, _val_data, _test_data