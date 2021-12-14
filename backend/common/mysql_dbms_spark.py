"""
Tools for performing operations on MySQL database
"""
import pyodbc


class MysqlDbms:

    def __init__(self, endpoint, db, table, username, password):
        self.endpoint = endpoint
        self.db = db
        self.table = table
        # pyodbc connection str ing
        driver = "{Amazon Redshift}"
        self.conn = pyodbc.connect("Driver={}; "
                              "Server={}; "
                              "Database={}; "
                              "UID={}; "
                              "PWD={}; "
                              "Port=5439".format(driver, self.endpoint, self.db, username, password))
        self.cursor = self.conn.cursor()

    def add(self, col_to_val):
        """
        @param col_to_val:  dict of column name to value
        @return: <boolean> success
        """
        cols_str = str(tuple(col_to_val.keys())).replace("'", '')
        vals_str = str(tuple(col_to_val.values()))
        sql = """INSERT INTO {} {} VALUES {}""".format(self.table, cols_str, vals_str)
        # print('sql: ', sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            print('error when adding to db')
            print(Exception)
            return False
        pass

    def delete(self, index):
        """
        @param index: index to delete
        @return: <boolean> success
        """

        pass

    def query(self, query_str):
        """
        @param query_str: <str> sql query
        @return: <boolean> success
                 <dict> result
        """
        try:
            self.cursor.execute(query_str)
            return True, self.cursor.fetchall()
        except:
            return False, None
        pass

    def update(self, db_index, col_to_val=None):
        """
        @param db_index: index of row
        @param col_to_val: dict of column name to new value
        @return: <boolean> success
        """

        if col_to_val is None:
            col_to_val = {}
        pass


if __name__ == "__main__":
    dbms = MysqlDbms('redshift-cluster-1.c26kfcowhljw.us-west-1.redshift.amazonaws.com', 'covid_19', 'c_19_cases')
    query_str = """select sex, count(*) as count from c_19_cases group by sex;"""
    _, result = dbms.query(query_str)
    print(result)
    print(type(result))
    pass