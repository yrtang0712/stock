import os
import pandas as pd
import numpy as np
import load_md as foo
import time

def dataset(year, month, days=None, codes=['000002']):
    if not days:
        days = 23

    keys = ['totbid', 'totoff', 'vol']
    keys.extend(['last', 'low', 'high'])
    keys.extend(['bid' + str(x) for x in range(1, 11)])
    keys.extend(['ask' + str(x) for x in range(1, 11)])
    keys.extend(['bid_vol' + str(x) for x in range(1, 11)])
    keys.extend(['ask_vol' + str(x) for x in range(1, 11)])

    data = pd.DataFrame()

    df = read_data(year, month, days, codes, keys)
    t = time.time()
    for c in codes:
       
        temp = pd.DataFrame(df[c].values)
        temp.columns = keys
        temp['code'] = c
        

        temp['vol'] = temp['vol'].diff().fillna(0)
        temp['vol'][temp['vol'] < 0] = 0

        # for i in range(1, 11):
        #     df.eval('ask_amt%s=ask%s*ask%s' % (str(i), str(i), str(i)), inplace=True)
        # for i in range(1, 11):
        #     df.eval('bid_amt%s=bid%s*bid%s' % (str(i), str(i), str(i)), inplace=True)

        temp['ask'] = temp[['ask' + str(x) for x in range(1, 11)]].mean(axis=1)
        temp['bid'] = temp[['bid' + str(x) for x in range(1, 11)]].mean(axis=1)
        temp.drop(['ask' + str(x) for x in range(1, 11)], axis=1, inplace=True)
        temp.drop(['bid' + str(x) for x in range(1, 11)], axis=1, inplace=True)

        temp['ask_vol'] = temp[['ask_vol' + str(x) for x in range(1, 11)]].mean(axis=1)
        temp['bid_vol'] = temp[['bid_vol' + str(x) for x in range(1, 11)]].mean(axis=1)
        temp.drop(['ask_vol' + str(x) for x in range(1, 11)], axis=1, inplace=True)
        temp.drop(['bid_vol' + str(x) for x in range(1, 11)], axis=1, inplace=True)

        m_lst = ['last', 'bid', 'ask']
        for i in m_lst:
            temp[i+'_mean'] = temp[i].ewm(span=4).mean()
            temp.drop(i, axis=1, inplace=True)

        for i in range(temp.shape[0]//4802):
            data = data.append(temp[i*4802:(i+1)*4802][::100])
    print('Finished, cost %.3fs' % (time.time()-t))

    return data

def read_data(year, month, days, codes=['000002'], keys=None):
    result = pd.DataFrame()
    int64_keys = ['amount', 'totbid', 'totoff', 'vol']
    float_keys = ['last', 'low', 'high', 'open', 'avebid', 'aveoff', 'trade']
    float_keys.extend(['bid' + str(x) for x in range(1, 11)])
    float_keys.extend(['ask' + str(x) for x in range(1, 11)])
    float_keys.extend(['bid_vol' + str(x) for x in range(1, 11)])
    float_keys.extend(['ask_vol' + str(x) for x in range(1, 11)])
    if keys:
        int64_keys = list(set(keys) & set(int64_keys))
        float_keys = list(set(keys) & set(float_keys))
    j = 0
    for d in range(1, 32):
        if not os.path.exists(os.path.join('/data/stock/newSystemData/rawdata/wind/stock_eod/', 
                str(year), str('%02d' % month), str(year*10000+month*100+d) + '.csv')):
            continue 
        j += 1
        if j > days:
            break
        t1 = time.time()
        data = pd.DataFrame()
        for i in int64_keys:
            df = foo.get_md_by_tick(year*10000+month*100+d, i, codes=codes, dtype='int64').astype('float32')
            data = pd.concat([data, df], axis=1)

        for i in float_keys:
            df = foo.get_md_by_tick(year*10000+month*100+d, i, codes=codes, dtype='float32')
            data = pd.concat([data, df], axis=1)

        data.index = (month*100+d)*1000000+data.index//1000
        result = result.append(data)
        print('Finished %d-%d-%d, cost %.3fs' % (year, month, d, time.time() - t1))
    return result

def get_data(d=0):
    data = pd.read_csv('/data/dataDisk1/yaru/data/data_18.csv', index_col=0).groupby('code')
    target = pd.read_csv('./data/target_18.csv').groupby('code')

    codes = pd.read_csv('./data/code.csv', index_col=0).code.values
    x_train, y_train, x_test, y_test = [], [], [], []
    for c in codes:
        df = data.get_group(c)
        obj = target.get_group(c)

        df.drop('code', axis=1, inplace=True)

        if df.isnull().sum().max() >= 49:
            continue
        df = df.fillna(method='bfill').fillna(method='ffill')
        df = df.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
        for j in range(d+15,d+109):
            if j < d+105:
                x_train.append(df[(j-5)*49:j*49].values)
                y_train.append(obj['change'][j:j+1].values)
            elif j == d+105:
                pass
            else:
                x_test.append(df[(j-15)*49:j*49].values)
                y_test.append(obj['change'][j:j+1].values)

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    # y_train = (y_train - y_train.min()) / (y_train.max() - y_train.min())
    y_train = y_train / 20 + 0.5
    np.clip(y_train, 0, 1)
    
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    # y_test = (y_test - y_test.min()) / (y_test.max() - y_test.min())
    y_test = y_test / 20 + 0.5
    np.clip(y_test, 0, 1)
    return x_train, y_train, x_test, y_test

def read_target(year, month=1):
    df = pd.read_csv('/data/dataDisk1/yaru/data_2/target_2.csv', index_col=0) # /home/sharedFold/fwd_return/return_1d.csv
    df.columns = ['date', 'code', 'change']

    target = pd.DataFrame()
    for day in range(1, 32):
        target = target.append(df[df.date == year*10000+month*100+day])

    return target

def get_zz():
    df = pd.read_csv('/data/dataDisk1/yaru/data/zzzs.csv', index_col=0)
    target = pd.DataFrame(df.change.values, columns=['change'])

    x, y = [], []
    for i in range(21, df.shape[0]):
        x.append(df[i-21:i-1].values)
        y.append(target['change'][i:i+1].values)

    x = np.array(x)
    y = np.array(y)
    x_train, y_train, x_test, y_test = x[:-20], y[:-20], x[-20:], y[-20:]
    
    return x_train, y_train, x_test, y_test
    
# codes = []
# with open(os.path.join('/data/stock/newSystemData/rawdata/universe/TOP2000', '20190102')) as f:
#     for c in f:
#         codes.append(c.strip())

# for i in range(1, 5):
#     for j in range(1, 32):
#         path = os.path.join('/data/stock/newSystemData/rawdata/universe/TOP2000', '2019%02d%02d' % (i, j))
#         if os.path.exists(path):
#             lst = []
#             with open(path) as f:
#                 for c in f:
#                     lst.append(c.strip())
#             codes = list(set(lst) & set(codes))

# codes = sorted(codes)
# df = pd.DataFrame({'code': codes})
# print(df.shape)
# df.to_csv('./code/code_19.csv')

# df = pd.read_csv('/home/sharedFold/fwd_return/return_1d.csv')
# df.columns = ['date', 'code', 'change']
# df['date'] = pd.to_datetime(df['date'])
# df.set_index('date', inplace=True)
# print(df.isnull().sum())
# df = df['2018-01':'2018-03']