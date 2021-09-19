import pandas as pd
from sqlalchemy import create_engine, inspect


class db_helper:
    def __init__(self, host='localhost', user='root', password='root', db='db'):
        # Sqlalchemy connection
        engine_str = f'mysql+pymysql://{user}:{password}@{host}/{db}'
        self.engine = create_engine(engine_str)
        
    def get_tables(self):
        query = self.engine.execute('SHOW TABLES')
        return [item for tupl in query.fetchall() for item in tupl]
    
    def has_table(self, table):
        return inspect(self.engine).has_table(table)
            
    def get_data_between_dates(self, table, start, end):
        sql = f'''SELECT * FROM {table}
                WHERE Date BETWEEN '{start}' AND '{end}'
                ORDER BY Date'''
        return pd.read_sql(sql, con=self.engine)
    
    def count_rows(self, table, start, end):
        sql = f'''SELECT COUNT(*) FROM {table}
                WHERE Date BETWEEN '{start}' AND '{end}';'''
        return self.engine.execute(sql).fetchall()[0][0]
    
    def df_to_sql(self, df, table, id_):
        # if_exists='append' -> If table exists: Insert new values to the existing table.
        df.to_sql(table.lower(), self.engine, if_exists='append', index=True, index_label=id_)