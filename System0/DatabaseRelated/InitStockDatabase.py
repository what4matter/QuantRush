"""
概要：
    建立股票数据库，一支股票一个表，表名为股票代码。
    表中包含一支股票最近40天的各种数据（开盘价，收盘价，...）
    该模块实现一键创建和更新数据库，但是有内存泄漏的问题，比如有一只股票下架了，需要将其从数据库中清除。
"""


from Connection import Conn
import akshare as ak
import pandas as pd
from datetime import date, timedelta
from sqlalchemy import create_engine


# 将日期类转化为合适格式的字符串类型
def date_to_str(date):
    ret = None  # 返回值
    if(date.month < 10):
        ret = str(date.year) + '0' + str(date.month)
    else:
        ret = str(date.year) + str(date.month)

    if(date.day < 10):
        ret += '0' + str(date.day)
    else:
        ret += str(date.day)
    
    return ret


# 数据库连接参数
config = {
    'host': 'localhost',        # 数据库主机地址
    'port': 3306,               # 数据库端口号
    'user': 'root',             # 数据库用户名
    'password': 'root',         # 密码
    'database': 'mysql'         # 连接到mysql数据库 
}


# 定义要创建的数据库名称
db_name = 'stock'


if __name__=='__main__':
    day = date.today()      # 拿到当天日期
    end_time = day - timedelta(days=1)  # 拿到前一天的日期
    start_time = end_time - timedelta(days=40) # 保证拿到24天以内的有效数据即可
    # 类型转化
    end_time = date_to_str(end_time)
    start_time = date_to_str(start_time)

    # 不加载京A板块
    data_curs_h = ak.stock_sh_a_spot_em()  # 获取沪A股实时数据
    data_curs_s = ak.stock_sz_a_spot_em()  # 获取深A股实时数据
    data_curs = pd.concat([data_curs_h, data_curs_s], ignore_index=True) # 连接两个DataFrame

    # 创建数据库操作实体
    conn = Conn(**config)
    # 连接数据库
    conn.connect()
    # 创建数据库
    conn.create_database(db_name)
    # 关闭连接
    conn.close()

    # 创建数据库引擎
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{db_name}')

    i = 1
    total = data_curs.shape[0]
    # 遍历所有股票
    for row in data_curs.itertuples(index=False, name='Pandas'):
        print('---------------------------- 当前进度: ', i, ' [总票数：', total, ']', end='\r', flush=True)
        i += 1

        code = getattr(row, '代码')     # 股票代码
        data_hist = ak.stock_zh_a_hist(symbol=code, period='daily', start_date=start_time, end_date=end_time, adjust='qfq')
        
        # 如果数据为空就跳过，避免插入空数据（mysql会报错）
        if data_hist.empty:
            continue

        # 插入数据库，建表
        data_hist.to_sql(name=code, con=engine, if_exists='replace', index=False)
    
    engine.dispose()