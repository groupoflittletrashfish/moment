import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class DatabaseSession:
    def __init__(self):
        # 创建数据库引擎
        self.engine = create_engine('mysql+pymysql://root:Lwm%401e5ghj9@139.224.163.144:3306/noname')
        # 创建Session工厂,注意此处是指工厂，如果是生成实例，则是self.Session()
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def insert(self, model):
        session = self.get_session()
        try:
            session.add(model)
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def insert_batch(self, model_list):
        session = self.get_session()
        try:
            session.add_all(model_list)
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def query_all(self, model):
        session = self.get_session()
        try:
            result = session.query(model).all()
            return result
        except SQLAlchemyError:
            return []
        finally:
            session.close()

    def delete(self, model):
        """删除一条记录"""
        session = self.get_session()
        try:
            session.delete(model)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
        finally:
            session.close()

    def update(self, model):
        """更新一条记录"""
        session = self.get_session()
        try:
            session.merge(model)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
        finally:
            session.close()

    def read_sql(self, query, params=None):
        return pd.read_sql_query(sql=query, con=self.engine, params=params)

    @staticmethod
    def page(index, offset):
        index = int(index)
        offset = int(offset)
        if index <= 0:
            index = 1
        page = (index - 1) * offset
        return {
            'page': page,
            'offset': offset
        }
