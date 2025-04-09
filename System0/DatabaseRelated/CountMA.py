"""
概要：
    计算每一支股票的均线数据，并将其储存在数据库ma中，
    每一支股票的均线数据对应一张表
"""


from Connection import Conn
import pandas as pd
from sqlalchemy import create_engine


# 数据库连接参数
config = {
    'host': 'localhost',        # 数据库主机地址
    'port': 3306,               # 数据库端口号
    'user': 'root',             # 数据库用户名
    'password': 'root',         # 密码
    'database': 'mysql'         # 连接到mysql数据库 
}


# 定义要创建的数据库名称
db_name = 'ma'


# 计算某只股票的均线数据MA
def MA(data):
    ret = {}
    ret['20日均线'] = data['收盘'].rolling(window=20).mean()  # 20日均线
    ret['10日均线'] = data['收盘'].rolling(window=10).mean()  # 10日均线
    ret['5日均线'] = data['收盘'].rolling(window=5).mean()  # 5日均线
    ret = pd.DataFrame(ret)
    ret = ret.fillna(0)     # 把所有nan填充成0
    ret = ret.round(2)      # 保留两位小数
    return ret


if __name__=='__main__':
    # 1. 拉取数据库中所有股票的历史数据，并计算均线数据ma
    # 创建数据库引擎，连接stock数据库
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/stock')
    # 获取数据库中所有表的名称
    query = "show tables"
    tables = pd.read_sql(query, con=engine)

    ma_list = {}    # 储存所有股票的ma数据
    i = 1
    total = tables.shape[0]
    for row in tables.itertuples(index=False, name='Pandas'):
        print('---------------------------- 读取历史数据并计算ma的进度: ', i, ' [总票数：', total, ']', end='\r', flush=True)
        i += 1
        table = row[0]  # 表名，str类型
        query = f"select * from `{table}`"
        data = pd.read_sql(query, con=engine)
        ma = MA(data)       # ma 是Dataframe类型的数据
        ma_list[table] = ma

    engine.dispose()

    print()

    # 2. 创建数据库ma（如果没有的话）
    # 创建数据库操作实体
    conn = Conn(**config)
    # 连接数据库
    conn.connect()
    # 创建数据库
    conn.create_database(db_name)
    # 关闭连接
    conn.close()


    # 3. 将均线数据ma入库
    # 连接ma库
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{db_name}')
    # 建表入库
    i = 1
    for key, value in ma_list.items():
        print('---------------------------- ma入库进度: ', i, ' [总票数：', total, ']', end='\r', flush=True)
        i += 1
        value.to_sql(name=key, con=engine, if_exists='replace', index=False)
    
    engine.dispose()
