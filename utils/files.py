import pandas as pd

def save_data_to_file(_data, path, _symbol, _timeframe):
    _data.columns = ['date','open','high','low','close','volume']
    _data = _data.sort_values(by='date')
    _data = _data.drop_duplicates(subset='date').reset_index(drop=True)
    _data['date'] = pd.to_datetime(_data['date'], unit='ms')
    _data.to_csv(path + _symbol.replace('/', '_') + '_' + _timeframe + '.csv', index=False)

def read_data_from_file(path, _symbol, _timeframe):
    _df = pd.read_csv(path + _symbol.replace('/', '_') + '_' + _timeframe + '.csv')
    _df = _df.sort_values(by='date')
    _df = _df.drop_duplicates(subset='date').reset_index(drop=True)
    _df['date'] = pd.to_datetime(_df['date'])
    _df.set_index('date', inplace=True)
    # Удалим значения где нет объемов
    _df = _df.drop(_df[_df['volume']==0.0].index)
    return _df