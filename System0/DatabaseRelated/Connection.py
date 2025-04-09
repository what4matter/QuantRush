"""
封装数据库操作接口
"""

import pymysql


class Conn:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.databse = database
        self.connection= None

    def connect(self):
        # 创建数据库连接
        self.connection = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, database=self.databse)

    def create_database(self, db_name):
        # 创建数据库
        with self.connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            create_db_sql = f"create database if not exists {db_name}"
            cursor.execute(create_db_sql)
            self.connection.commit()

    def use(self, db_name):
        # 切换数据库
        self.connection.select_db(db_name)
    
    def close(self):
        # 关闭数据库连接
        self.connection.close()