import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from load_data import dataset, read_target
from label import get_lab
import os

# df = pd.read_csv('test.csv', index_col=0)
# a = []
# j = 10
# for i in range(j):
#     a.append(df[i::j].corr().values.mean()*2-1)    # only caculate the correlation of 'pred' and 'change'
# a = np.array(a)
# print(a)
# print(a.mean())

# df = pd.read_csv('./code/code_19.csv', index_col=0)
# codes = []
# for i in range(df.shape[0]):
#     codes.append('%06d'% df['code'][i:i+1].values[0])

# for i in range(1, 5):
#     data = dataset(2019, i, codes=codes)
#     print(data.shape)
#     data.to_csv('/data/dataDisk1/aoqi/data/data_19%02d.csv' % i)

# target = pd.DataFrame()
# for i in range(1, 13):
#     df = read_target(2018, i)
#     df['change'] = df['change'].apply(lambda x: x*100)
#     print(df.shape)
#     target = target.append(df)
# print(target.shape)
# target.to_csv('./data/target_18.csv')

# data = pd.DataFrame()
# for i in range(1, 5):
#     df = pd.read_csv('/data/dataDisk1/aoqi/data/data_s%d.csv' % i, index_col=0)
#     data = data.append(df)
# print(data.shape)
# data.to_csv('/data/dataDisk1/aoqi/data/data_18.csv')

# codes = []
# with open(os.path.join('/data/stock/newSystemData/rawdata/universe/TOP2000', '20190102')) as f:
#     for c in f:
#         codes.append(c.strip())

# codes = sorted(codes)
# df = pd.DataFrame({'code': codes})
# print(df.shape)
# df.to_csv('./data/code.csv')


# path1 = "/home/yaru/workspace/data"
# file_path = path1 + '/' + 'label' + '.csv'
# label = get_lab()
# label = label.fillna(value=0)
# date_list = label.columns.values
# codes_list = label.index.values

# f = open(file_path,'w')

# for date in date_list:
#     for code in codes_list:
#         line = str(date) + '\t' + str(code) + '\t' + '\t' + str(label.loc[code, date]) + '\n'
#         f.writelines(line)
    
# f.close()


# target = pd.DataFrame()
# df = pd.read_csv('./data/label.csv')
# df.columns = ['raw']
# df['date'] = df['raw'].apply(lambda x: x.split('\t')[0])
# df['code'] = df['raw'].apply(lambda x: x.split('\t')[1])
# df['change'] = df['raw'].apply(lambda x: x.split('\t')[-1])
# df.drop('raw', axis=1, inplace=True)
# # print(df.head())
# df.to_csv('./data/target.csv')


