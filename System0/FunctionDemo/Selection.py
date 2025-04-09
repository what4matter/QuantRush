"""
抽象出一个选择器类，如果一个股票满足要求就返回True，反之返回False
选择器中有三个属性：
    1. hist_data历史数据
    2. cur_data当前数据
    3. ma历史+实时均线数据
"""


import pandas as pd
import numpy as np


# 计算当前实时均线cur_ma
def count_cur_ma(hist_data, cur_data, ma):
    hist_close_price = hist_data['收盘']    # 历史收盘价
    cur_close_price = getattr(cur_data, '最新价') # 当前现价

    ret = {}
    cur_20day = (hist_close_price.tail(19).sum() + cur_close_price) / 20    # 最新20天线数据
    cur_10day = (hist_close_price.tail(9).sum() + cur_close_price) / 10     # 最新10天线数据
    cur_5day = (hist_close_price.tail(4).sum() + cur_close_price) / 5       # 最新5天线数据
    cur_20day = np.round(cur_20day, 2)
    cur_10day = np.round(cur_10day, 2)
    cur_5day = np.round(cur_5day, 2)

    ret['20日均线'] = [cur_20day]
    ret['10日均线'] = [cur_10day]
    ret['5日均线'] = [cur_5day]
    ret = pd.DataFrame(ret)
    ma = pd.concat([ma, ret], ignore_index=True)
    return ma


class Sel:
    def __init__(self, hist_data, cur_data, ma):
        self.hist_data = hist_data  # Dataframe
        self.cur_data = cur_data    # 命名元组
        self.ma = count_cur_ma(hist_data, cur_data, ma)                # Dataframe
    
    def select(self, *args):
        for func in args:
            if(not func(hist_data=self.hist_data, cur_data=self.cur_data, ma=self.ma)):
                return False
        
        return True