"""
Tools for performing operations on MySQL database
"""


class MysqlDbms:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def add(self, col_to_val=None):
        """
        @param col_to_val:  dict of column name to value
        @return: <boolean> success
        """

        if col_to_val is None:
            col_to_val = {}
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
