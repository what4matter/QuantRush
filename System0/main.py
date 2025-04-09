"""
选股主程序
"""

import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from FunctionDemo.Selection import Sel
from FunctionDemo.FunctionSet import *
import csv


# 数据库连接参数
config = {
    'host': 'localhost',        # 数据库主机地址
    'port': 3306,               # 数据库端口号
    'user': 'root',             # 数据库用户名
    'password': 'root',         # 密码
    'database': 'mysql'         # 默认连接到mysql数据库 
}


# 保存数据
def save(data, filename):
    # 保存数据
    with open(f'Result/{filename}', 'w', newline='', encoding='utf-8') as csvfile:
        # 创建一个csv的写入器
        writer = csv.writer(csvfile)
        # 遍历字典中的每个键值对
        for key, value in data.items():
            # 写入键值对
            writer.writerow([key, value])


def run(funcset):
    # 不加载京A板块
    data_curs_h = ak.stock_sh_a_spot_em()  # 获取沪A股实时数据
    data_curs_s = ak.stock_sz_a_spot_em()  # 获取深A股实时数据
    data_curs = pd.concat([data_curs_h, data_curs_s], ignore_index=True) # 连接两个DataFrame

    # 创建数据库引擎，连接stock表
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database"]}')

    ret = {}    # 存储最后的筛选结果
    i = 1
    total = data_curs.shape[0]
    # 遍历所有股票
    for row in data_curs.itertuples(index=False, name='Pandas'):
        print('---------------------------- 当前筛选进度: ', i, ' [总票数：', total, ']', end='\r', flush=True)
        i += 1

        code = getattr(row, '代码')
        name = getattr(row, '名称')
        sql = f'select * from stock.{code}'

        # 处理停牌票（停牌票没有最新价）
        if pd.isna(getattr(row, '最新价')):
            continue

        # 处理掉即将退市的*票
        if name[0] == '*':
            continue

        # 处理查询的表不存在的情况
        try:
            hist_data = pd.read_sql(sql, con=engine)    
        except DatabaseError:
            hist_data = pd.DataFrame()  # 返回一个空的DataFrame

        if hist_data.empty:
            continue

        sql = f'select * from ma.{code}'
        ma = pd.read_sql(sql, con=engine)
        # 实例化选择器类
        sel = Sel(cur_data=row, hist_data=hist_data, ma=ma)
        # 传入选股函数，执行select方法
        flag = sel.select(*(funcset.funcs))
        # 存储选出的股票
        if flag:
            ret[code] = name

    print()
    engine.dispose()
    # 保存筛选结果
    save(ret, funcset.filename)


if __name__=="__main__":
    # run(GoldencrossCombination1)
    # run(GoldencrossCombination2)
    # run(GoldencrossCombination3)
    # run(GoldencrossCombination4)
    # run(ExtremeReversal)
    # run(SmallLineType1)
    # run(SmallLineType2)
    # run(SmallLineType3)
    run(CloseToLine)
