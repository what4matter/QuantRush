"""
该模块中存取各种方法的组合
"""

from FunctionDemo.Function import Func


"""
金叉翻线组合1：
    1. 金叉
    2. 5跟10同向，20不同向
    3. 收盘价站上5天线和20天线
    4. 20天线在10天线上方
"""
class GoldencrossCombination1:
    filename = 'GoldencrossCombination1.csv'
    funcs = [
        Func.cur_golden_cross, 
        Func.ma20_different_direction, 
        Func.close_price_on20and5, 
        Func.ma20_on_ma10,
        Func.withoutGEM,
        Func.withoutST
    ]


"""
金叉翻线组合2：
    1. 金叉
    2. 5跟20同向，10不同向
    3. 收盘价站上5和20天线
    4. 20天线大于10天线
"""
class GoldencrossCombination2:
    filename = 'GoldencrossCombination2.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.cur_golden_cross,
        Func.ma10_different_direction,
        Func.close_price_on20and5,
        Func.ma20_on_ma10
    ]


"""
金叉翻线组合3：
    1. 金叉
    2. 三线同向
    3. 价格站上5天线和20天线
    4. 20天线大于10天线
"""
class GoldencrossCombination3:
    filename = 'GoldencrossCombination3.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.cur_golden_cross,
        Func.three_lines_in_same_direction,
        Func.close_price_on20and5,
        Func.ma20_on_ma10
    ]

"""
金叉翻线组合4，复杂情况：
    先看前一天是否金叉：
      1. 金叉：再看当天是否三线同向：
          a. 当天三线同向，pass
          b. 当天没有三线同向，再看当天是否金叉：
              1). 没有金叉，pass
              2). 金叉，再看价格是否在均线之上
                  在均线之上，return True；不再均线之上，pass
      2. 不金叉：再看今天是否金叉
          a. 不金叉，pass
          b. 金叉，再看今天是否三线同向：
              1). 当天没有三线同向，pass
              2). 当天三线同向，再看价格是否站上均线：
                  站上return True，没站上pass
"""
class GoldencrossCombination4:
    filename = 'GoldencrossCombination4.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.golden_cross_complex
    ]


"""
极端反转：
    1. 5,10,20三线同向
    2. 三线从高到低20,10,5
    3. 价格站上20天线
    4. 20天线大于10天线
"""
class ExtremeReversal:
    filename = 'ExtremeReversal.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.three_lines_in_same_direction,
        Func.ma20_ma10_ma5_from_high_to_low,
        Func.close_price_on20
    ]


"""
小线型组合1：
    1. 5,10,20依次从高到低排列，连续五天
    2. 小线型：当日开盘价和收盘价之差比值不超过5%
    3. 靠近五天线：当日收盘价与当日五天线之差比值不超过3%
    4. 收盘价站上5天线
    5. 连续5天3线同向
"""
class SmallLineType1:
    filename = 'SmallLineType1.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.ma5_ma10_ma20_from_high_to_low_fivedays,
        Func.small_line_type,
        Func.close_to_ma5,
        Func.close_price_on5,
        Func.three_lines_in_same_direction_fivedays
    ]


"""
小线型组合2：
    1. 三线同向连续两天
    2. 5,20,10一次从高到排列连续两天
    3. 小线型：当日开盘价和收盘价之差比值不超过5%
    4. 靠近五天线：当日收盘价与当日五天线之差比值不超过3%
    5. 收盘价站上5天线
"""
class SmallLineType2:
    filename = 'SmallLineType2.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.three_lines_in_same_direction_towdays,
        Func.ma5_ma20_ma10_from_high_to_low_towdays,
        Func.small_line_type,
        Func.close_to_ma5,
        Func.close_price_on5
    ]


"""
小线型组合3：
    1. 5跟10同向，20日不同向，连续两天
    2. 当天20在10上
    3. 当天收盘价和开盘价都站上5和20天线
    4. 小线型
    5. 靠近5天线
"""
class SmallLineType3:
    filename = 'SmallLineType3.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.ma20_different_direction_towdays,
        Func.ma20_on_ma10,
        Func.open_and_close_price_on5and20,
        Func.small_line_type,
        Func.close_to_ma5
    ]


"""
贴线组合：
    1. 连续10天以上20天线依次上涨
    2. 当日最低价或者收盘价与20天线的差值比率不超过1%
"""
class CloseToLine:
    filename = 'CloseToLine.csv'
    funcs = [
        Func.withoutGEM,
        Func.withoutST,
        Func.ma20_continuous_increase,
        Func.closeORlow_close_to_ma20
    ]