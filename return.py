#!/usr/bin/python
import sys,os
#import commands
import re
import pandas as pd
#sys.path.append('/home/sharedFold/WinQ/')
import IndexData as ID

path1 = '/data/stock/newSystemData/rawdata/wind/stock_eod'
path2 = '/home/yaru/workspace/label'

def get_1day_data(day):
	data = {}
	sday = str(day)
	year = sday[:4]
	month = sday[4:6]
	day_path = path1 + '/' + str(year) + '/' + str(month) + '/' + str(sday) + '.csv'
	f = open(day_path,'r')
	lines = f.readlines()
	for line in lines:
		sline = line.strip()
		if sline == '':
			continue
		items = re.split('\s+',sline)
		stock = str(items[0])
		oo = float(items[1])
		cc = float(items[4])
		isopen = int(items[-3])
		adj = float(items[-2])
		data[stock] = {}
		data[stock]['isopen'] = isopen
		data[stock]['adj'] = adj
		data[stock]['open'] = oo
		data[stock]['close'] = cc
	f.close()

	return data
      
# def get_1day_ret(day):
# 	#lastday = IndexData().get_front_day(str(day))
# 	lastday = day_list[ day_list.index( day ) - 1]
# 	print ( 'lastday', lastday )
# 	data1 = get_1day_data(lastday)
# 	data = get_1day_data(day)

# 	print ( data1['600276']['isopen'],data1['600276']['adj'],data1['600276']['open'],data1['600276']['close'] )
# 	print ( data['600276']['isopen'],data['600276']['adj'],data['600276']['open'],data['600276']['close'] )
# 	print ( data['600276']['close'] / data['600276']['adj'] / data1['600276']['close'] )


if __name__ == '__main__':
	start_day = '20150101'
	end_day = '20190801'
	day_list = ID.get_deal_day_list_in_period(start_day,end_day)
	# print(day_list)
	global_info_dict = {}

	for day in day_list:
		file_path = path2 + '/' + str(day) + '.csv'
		# print (file_path)
		f = open(file_path,'w')

		if day != day_list[-1]:
			day = day_list[day_list.index(day) + 1]
			data = get_1day_data(day)
			for stock in data:
				#do not calculate return FirstTime
				FirstTime = False
				#default line
				line = stock + '\tnan\tnan\n'
				if (not stock in global_info_dict) and data[stock]['isopen']:
					global_info_dict[stock] = {}
					FirstTime = True
				if not FirstTime:
					if data[stock]['isopen']:
						#print day,stock
						ret_c_c = data[stock]['close'] / data[stock]['adj'] / global_info_dict[stock]['last_real_close'] - 1.0
						ret_o_o = data[stock]['open'] / data[stock]['adj'] / global_info_dict[stock]['last_real_open'] - 1.0
						line = stock + '\t' + str(ret_c_c) + '\t' + str(ret_o_o) + '\n'
						#print(line)
				f.writelines(line)
				#refresh global info
				if data[stock]['isopen']:
					global_info_dict[stock]['last_trade_day'] = day
					global_info_dict[stock]['last_real_open'] = data[stock]['open']
					global_info_dict[stock]['last_real_close'] = data[stock]['close']

		else:
			data = get_1day_data(day)
			for stock in data:
				line = stock + '\tnan\tnan\n'
				f.writelines(line)

		f.close()
