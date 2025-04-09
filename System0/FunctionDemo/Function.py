"""
概要：
    本模块提供筛选股票的函数，每个函数有且仅有三个参数
    1. hist_data历史数据
    2. cur_data当前数据
    3. ma历史+实时均线数据
"""


# 是否金叉（是返回True）
def golden_cross(ma):
    # 如果这只票的历史数据连11天都不到，直接pass，因为10天线都算不出来
    if ma.shape[0] < 11:
        return False
    
    ma5 = ma['5日均线']
    ma10 = ma['10日均线']

    ma5 = ma5.tail(2).reset_index(drop=True)
    ma10 = ma10.tail(2).reset_index(drop=True)

    if ma5[0] <= ma10[0] and ma5[1] >= ma10[1]:
        return True
    else:
        return False


class Func:
    """------------------------------  一级过滤板块  -------------------------"""
    # 是否筛掉ST板块（是ST板块返回False）
    @staticmethod
    def withoutST(hist_data, cur_data, ma):
        name = getattr(cur_data, '名称')
        if 'ST' in name:
            return False
        else:
            return True
        
    # 是否筛掉创业板块（是创业板块返回False，不是返回True）
    @staticmethod
    def withoutGEM(hist_data, cur_data, ma):
        code = getattr(cur_data, '代码')
        if '68' in code or '3' in code:
            return False
        else:
            return True
        
    # 当天是否金叉（金叉返回True）
    @staticmethod
    def cur_golden_cross(hist_data, cur_data, ma):
        return golden_cross(ma)
    

    """---------------------------  收盘/开盘价板块  ---------------------------------"""
    # 收盘价是否站上20天线和5天线（站上返回True）
    @staticmethod
    def close_price_on20and5(hist_data, cur_data, ma):
        ma20 = ma['20日均线']
        ma5 = ma['5日均线']
        ma20 = ma20.tail(1).reset_index(drop=True)
        ma5 = ma5.tail(1).reset_index(drop=True)
        cur_price = getattr(cur_data, '最新价')
        if cur_price > ma20[0] and cur_price > ma5[0]:
            return True
        else:
            return False
        
    # 收盘价是否站上20天线（站上返回True）
    @staticmethod
    def close_price_on20(hist_data, cur_data, ma):
        ma20 = ma['20日均线']
        ma20 = ma20.tail(1).reset_index(drop=True)
        cur_price = getattr(cur_data, '最新价')
        if cur_price > ma20[0]:
            return True
        else:
            return False
        
    # 收盘价是否站上5天线（站上返回True）
    @staticmethod
    def close_price_on5(hist_data, cur_data, ma):
        ma5 = ma['5日均线']
        ma5 = ma5.tail(1).reset_index(drop=True)
        cur_price = getattr(cur_data, '最新价')
        if cur_price > ma5[0]:
            return True
        else:
            return False

    # 收盘价在所有均线之上（满足返回True）
    @staticmethod
    def close_price_onma(hist_data, cur_data, ma):
        ma20 = ma['20日均线']
        ma10 = ma['10日均线']
        ma5 = ma['5日均线']
        ma20 = ma20.tail(1).reset_index(drop=True)
        ma10 = ma10.tail(1).reset_index(drop=True)
        ma5 = ma5.tail(1).reset_index(drop=True)
        cur_price = getattr(cur_data, '最新价')
        if cur_price > ma20[0] and cur_price > ma10[0] and cur_price > ma5[0]:
            return True
        else:
            return False
    
    # 当天收盘价和开盘价都站上5和20天线
    @staticmethod
    def open_and_close_price_on5and20(hist_data, cur_data, ma):
        open_price = getattr(cur_data, '今开')
        cur_price = getattr(cur_data, '最新价')

        ma20 = ma['20日均线']
        ma5 = ma['5日均线']
        ma20 = ma20.tail(1).reset_index(drop=True)
        ma5 = ma5.tail(1).reset_index(drop=True)
        cur_price = getattr(cur_data, '最新价')
        if open_price > ma20[0] and open_price > ma5[0] and cur_price > ma20[0] and cur_price > ma5[0]:
            return True
        else:
            return False


    """------------------------  均线高低模块  --------------------------"""
    # 当天20天线是否在10天线上方（是返回True）
    @staticmethod
    def ma20_on_ma10(hist_data, cur_data, ma):
        ma20 = ma['20日均线']
        ma10 = ma['10日均线']
        ma20 = ma20.tail(1).reset_index(drop=True)
        ma10 = ma10.tail(1).reset_index(drop=True)
        if ma20[0] > ma10[0]:
            return True
        else:
            return False
        
    # 20,10,5是否从高到低排列（是返回True）
    @staticmethod
    def ma20_ma10_ma5_from_high_to_low(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma5 = ma['5日均线']
        ma10 = ma['10日均线']
        ma20 = ma['20日均线']

        ma5 = ma5.tail(1).reset_index(drop=True)
        ma10 = ma10.tail(1).reset_index(drop=True)
        ma20 = ma20.tail(1).reset_index(drop=True)

        if ma5[0] <= ma10[0] <= ma20[0]:
            return True
        else:
            return False
    
    # 5,10,20依次从高到低排列（满足返回True）
    @staticmethod
    def ma5_ma10_ma20_from_high_to_low(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma5 = ma['5日均线']
        ma10 = ma['10日均线']
        ma20 = ma['20日均线']

        ma5 = ma5.tail(1).reset_index(drop=True)
        ma10 = ma10.tail(1).reset_index(drop=True)
        ma20 = ma20.tail(1).reset_index(drop=True)

        if ma5[0] > ma10[0] > ma20[0]:
            return True
        else:
            return False
    
    # 5,10,20依次从高到低排列，连续5天（满足返回True）
    @staticmethod
    def ma5_ma10_ma20_from_high_to_low_fivedays(hist_data, cur_data, ma):
        n = 5

        if not Func.ma5_ma10_ma20_from_high_to_low(hist_data, cur_data, ma):
            return False
        
        i = 1
        while i <= n - 1:
            hist_data_crop = hist_data.iloc[:-i]
            ma_crop = ma.iloc[:-i]
            if not Func.ma5_ma10_ma20_from_high_to_low(hist_data_crop, cur_data, ma_crop):
                return False
            i = i + 1
        
        return True
    
    # 5,20,10依次从高到低排列（满足返回True）
    @staticmethod
    def ma5_ma20_ma10_from_high_to_low(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma5 = ma['5日均线']
        ma10 = ma['10日均线']
        ma20 = ma['20日均线']

        ma5 = ma5.tail(1).reset_index(drop=True)
        ma10 = ma10.tail(1).reset_index(drop=True)
        ma20 = ma20.tail(1).reset_index(drop=True)

        if ma5[0] > ma20[0] > ma10[0]:
            return True
        else:
            return False
    
    # 5,20,10依次从高到低排列，连续两天（满足返回True）
    @staticmethod
    def ma5_ma20_ma10_from_high_to_low_towdays(hist_data, cur_data, ma):
        n = 2  # n是几，就是连续几天

        if not Func.ma5_ma20_ma10_from_high_to_low(hist_data, cur_data, ma):
            return False
        
        i = 1
        while i <= n - 1:
            hist_data_crop = hist_data.iloc[:-i]
            ma_crop = ma.iloc[:-i]
            if not Func.ma5_ma10_ma20_from_high_to_low(hist_data_crop, cur_data, ma_crop):
                return False
            i = i + 1
        
        return True

    """---------------------------- 均线方向模块  ------------------------"""
    # 当天5跟20是否同向（同向返回True）
    @staticmethod
    def ma5_ma20_same_direction(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma5 = ma['5日均线']
        ma20 = ma['20日均线']

        ma5 = ma5.tail(2).reset_index(drop=True)
        ma20 = ma20.tail(2).reset_index(drop=True)

        k5 = ma5[1] - ma5[0]
        k20 = ma20[1] - ma20[0]

        if k5 > 0 and k20 > 0:
            return True
        else:
            return False
    
    # 当天是否三线同向（是返回True）
    @staticmethod
    def three_lines_in_same_direction(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma5 = ma['5日均线']
        ma10 = ma['10日均线']
        ma20 = ma['20日均线']

        ma5 = ma5.tail(2).reset_index(drop=True)
        ma10 = ma10.tail(2).reset_index(drop=True)
        ma20 = ma20.tail(2).reset_index(drop=True)

        k5 = ma5[1] - ma5[0]
        k10 = ma10[1] - ma10[0]
        k20 = ma20[1] - ma20[0]

        if k5 > 0 and k10 > 0 and k20 > 0:
            return True
        else:
            return False
    
    # 5,10同向，20不同向（满足返回True）
    @staticmethod
    def ma20_different_direction(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma5 = ma['5日均线']
        ma10 = ma['10日均线']
        ma20 = ma['20日均线']

        ma5 = ma5.tail(2).reset_index(drop=True)
        ma10 = ma10.tail(2).reset_index(drop=True)
        ma20 = ma20.tail(2).reset_index(drop=True)

        k5 = ma5[1] - ma5[0]
        k10 = ma10[1] - ma10[0]
        k20 = ma20[1] - ma20[0]

        if k5 > 0 and k10 > 0 and k20 < 0:
            return True
        else:
            return False
    
    # 20不同向，连续两天（满足返回True）
    @staticmethod
    def ma20_different_direction_towdays(hist_data, cur_data, ma):
        n = 2

        if not Func.ma20_different_direction(hist_data, cur_data, ma):
            return False
        
        i = 1
        while i <= n - 1:
            hist_data_crop = hist_data.iloc[:-i]
            ma_crop = ma.iloc[:-i]
            if not Func.ma20_different_direction(hist_data_crop, cur_data, ma_crop):
                return False
            i = i + 1
        
        return True
    
    # 5跟20同向，10不同向（满足返回True）
    @staticmethod
    def ma10_different_direction(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma5 = ma['5日均线']
        ma10 = ma['10日均线']
        ma20 = ma['20日均线']

        ma5 = ma5.tail(2).reset_index(drop=True)
        ma10 = ma10.tail(2).reset_index(drop=True)
        ma20 = ma20.tail(2).reset_index(drop=True)

        k5 = ma5[1] - ma5[0]
        k10 = ma10[1] - ma10[0]
        k20 = ma20[1] - ma20[0]

        if k5 > 0 and k20 > 0 and k10 < 0:
            return True
        else:
            return False

    # 当前5天线和10天线是否同向（同向返回True）
    @staticmethod
    def ma5_ma10_same_direction(hist_data, cur_data, ma):
        # 历史数据至少要有11天，才能算出两天的十天线
        if hist_data.shape[0] < 11:
            return False
        
        ma5 = ma['5日均线']
        ma10 = ma['10日均线']

        ma5 = ma5.tail(2).reset_index(drop=True)
        ma10 = ma10.tail(2).reset_index(drop=True)

        k5 = ma5[1] - ma5[0]
        k10 = ma10[1] - ma10[0]

        if k5 > 0 and k10 > 0:
            return True
        else:
            return False

    # 连续5天三线同向（满足返回True）
    @staticmethod
    def three_lines_in_same_direction_fivedays(hist_data, cur_data, ma):
        n = 5

        if not Func.three_lines_in_same_direction(hist_data, cur_data, ma):
            return False
        
        i = 1
        while i <= n - 1:
            hist_data_crop = hist_data.iloc[:-i]
            ma_crop = ma.iloc[:-i]
            if not Func.three_lines_in_same_direction(hist_data_crop, cur_data, ma_crop):
                return False
            i = i + 1
        
        return True

    # 连续2天三线同向（满足返回True）
    @staticmethod
    def three_lines_in_same_direction_towdays(hist_data, cur_data, ma):
        n = 2

        if not Func.three_lines_in_same_direction(hist_data, cur_data, ma):
            return False
        
        i = 1
        while i <= n - 1:
            hist_data_crop = hist_data.iloc[:-i]
            ma_crop = ma.iloc[:-i]
            if not Func.three_lines_in_same_direction(hist_data_crop, cur_data, ma_crop):
                return False
            i = i + 1
        
        return True
    
    # 20天线上涨
    @staticmethod
    def ma20_increase(hist_data, cur_data, ma):
        # 如果这只票的历史数据连21天都不到，直接pass，因为20天线都算不出来
        if hist_data.shape[0] < 21:
            return False
        
        ma20 = ma['20日均线']

        ma20 = ma20.tail(2).reset_index(drop=True)
        if ma20[1] >= ma20[0]:
            return True
        else:
            return False

    # 连续10天20天线依次上涨
    @staticmethod
    def ma20_continuous_increase(hist_data, cur_data, ma):
        n = 10

        if not Func.ma20_increase(hist_data, cur_data, ma):
            return False
        
        i = 1
        while i <= n - 1:
            hist_data_crop = hist_data.iloc[:-i]
            ma_crop = ma.iloc[:-i]
            if not Func.ma20_increase(hist_data_crop, cur_data, ma_crop):
                return False
            i = i + 1
        
        return True
    


    """----------------------- 距离板块  --------------------------"""
    # 小线型：当日开盘价和收盘价之差比值不超过n%（满足返回True）
    @staticmethod
    def small_line_type(hist_data, cur_data, ma):
        n = 0.05
        open_price = getattr(cur_data, '今开')
        close_price = getattr(cur_data, '最新价')
        if abs((close_price - open_price) / open_price <= n):
            return True
        else:
            return False
    
    # 靠近五天线：当日收盘价和当日5天线之差比值不超过n%（满足返回True）
    @staticmethod
    def close_to_ma5(hist_data, cur_data, ma):
        n = 0.03
        # 如果这只票的历史数据连6天都不到，直接pass，因为5天线都算不出来
        if hist_data.shape[0] < 6:
            return False
        
        ma5 = ma['5日均线']
        ma5 = ma5.tail(1).reset_index(drop=True)
        close_price = getattr(cur_data, '最新价')

        if abs((close_price - ma5[0]) / ma5[0]) <= n:
            return True
        else:
            return False


    @staticmethod
    def closeORlow_close_to_ma20(hist_data, cur_data, ma):
        dis = 0.01

        close = getattr(cur_data, '最新价')
        low = getattr(cur_data, '最低')

        ma20 = ma['20日均线']
        ma20 = ma20.tail(1).reset_index(drop=True)
        if ((abs(close - ma20[0]) / ma20[0]) <= dis or (abs(low - ma20[0]) / ma20[0]) <= dis):
            return False
        else:
            return True
    
    """---------------------- 复杂组合板块 ----------------------"""
    # 先看前一天是否金叉：
    #   1. 金叉：再看当天是否三线同向：
    #       a. 当天三线同向，pass
    #       b. 当天没有三线同向，再看当天是否金叉：
    #           1). 没有金叉，pass
    #           2). 金叉，再看价格是否在均线之上
    #               在均线之上，return True；不再均线之上，pass
    #   2. 不金叉：再看今天是否金叉
    #       a. 不金叉，pass
    #       b. 金叉，再看今天是否三线同向：
    #           1). 当天没有三线同向，pass
    #           2). 当天三线同向，再看价格是否站上均线：
    #               站上return True，没站上pass
    @staticmethod
    def golden_cross_complex(hist_data, cur_data, ma):
        ma_crop = ma.iloc[:-1]
        hist_data_crop = ma.iloc[:-1]
        if golden_cross(ma_crop):
            if Func.three_lines_in_same_direction(hist_data_crop, cur_data, ma_crop):
                return False
            elif Func.three_lines_in_same_direction(hist_data, cur_data, ma):
                if Func.close_price_onma(hist_data, cur_data, ma):
                    return True
        elif golden_cross(ma):
            if Func.three_lines_in_same_direction(hist_data, cur_data, ma):
                if Func.close_price_onma(hist_data, cur_data, ma):
                    return True
        
        return False
