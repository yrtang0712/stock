import pandas as pd
import re
import os

path = "/data/stock/newSystemData/rawdata/wind/stock_eod/"

def get_deal_day_list_in_period(start_day,end_day):
    date_list = []
    day_list = []

    for fpathe, _, fs in os.walk(path):
        for f in fs:
            tmp_path = os.path.join(fpathe, f)
            pattern = re.compile(r'20[0-1][0-9]+(\.[a-z]+)$')
            date = re.search(pattern, tmp_path)
            #print(date)
  
            if date!= None:
                date_value = date.group().split('.csv')
                date_value = date_value[0]
                date_list.append(date_value)
    date_list.sort()
    # print(date_list)

    new_date_list = [x.strftime('%Y%m%d') for x in list(pd.date_range(start_day, end_day))]

    for day in new_date_list:
        if day in date_list:
            day_list.append(day)
            
    return day_list
