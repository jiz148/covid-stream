from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import json
import os

import flask
from flask import Flask, jsonify, request
from flask_cors import CORS

from common.mysql_dbms_spark import MysqlDbms
from backend.kafka_utils.producer import produce

application = Flask(__name__)
# CORS
CORS(application)
# run producer


ENDPOINT = 'redshift-cluster-1.c26kfcowhljw.us-west-1.redshift.amazonaws.com'
DATABASE_NAME = 'covid_19'
TABLE_NAME = 'c_19_cases'
IGNORE_VALS = ['Missing', 'NA', None]
USER = os.getenv('RS_USER')
PSWD = os.getenv('RS_PSWD')



# state abv
with open('data/states_abv.json') as states_file:
    states_json = json.load(states_file)


@application.route('/getChartInfo', methods=['GET', 'POST'])
def case_endpoint():
    """
    post: receive json and add into database
    @return:
    """
    if request.method == 'POST':
        _add_to_db(request.get_json())
        res = {"success": True}
    else:
        res = _get_data_from_query()
        # print(res)
    return json.dumps(res)
    pass


def _add_to_db(cases_data):
    """
    @param cases_data: <json>
    @return: <boolean> success
    """
    print(cases_data)
    for case_data in cases_data:
        produce(case_data)
    pass


def _get_data_from_query():
    """
    @return: <boolean> success
             <json> data
    """
    today = datetime.now()
    months_before = today + relativedelta(months=-12)  # hard coded to be a year
    last_val, first_val = today.strftime('%Y-%m'), months_before.strftime('%Y-%m')

    # connect db
    dbms = MysqlDbms(ENDPOINT, DATABASE_NAME, TABLE_NAME, USER, PSWD)

    pie = _name_value_data(dbms, 'sex', ['Male', 'Female'])
    thermodynamic = _name_value_data(dbms, 'res_state')
    line = _line_data(dbms, first_val, last_val)
    vertical = _xy_data(dbms, 'age_group')
    crosswise = _xy_data(dbms, 'process')

    # for state names
    for state_dict in thermodynamic:
        abv = state_dict['name']
        state_name = states_json.get(abv)
        state_dict['name'] = state_name

    return {
        "pie": pie,
        "line": line,
        "thermodynamic": thermodynamic,
        "vertical": vertical,
        "crosswise": crosswise
    }


def _name_value_data(dbms, col_name, cases=None):
    """
    @param dbms: <db> dbms object
    @param col_name: <str> name of col
    @param cases: <list> list of cases eg. ['male', 'female']
    @return: <json> data
    """
    query_str = """select {}, count(*) as count from {} group by {}""".format(col_name, TABLE_NAME, col_name)
    _, query_result = dbms.query(query_str)
    # sample query_result: [('NA', 1244276), ('Female', 18846393), ('Male', 17160125), ('Other', 12)]
    result_dict = {}
    for row in query_result:
        result_dict[row[0]] = row[1]
    result = []
    if not cases:
        for key in result_dict.keys():
            if key not in IGNORE_VALS:
                result.append({"name": key, "value": result_dict[key]})
        return result
    for case in cases:
        if case not in IGNORE_VALS:
            result.append({"name": case, "value": result_dict[case]})
    return result
    pass


def _line_data(dbms, first_val, last_val, col_name='case_month'):
    """
    @param dbms: <db> dbms object
    @param first_val: <str> like '2021-12'
    @param last_val: <str> like '2021-12'
    @param col_name: <str> col name, optional
    @return: <json> data
    """
    query_str = """select {}, count(*) as count from {} group by {}""".format(col_name, TABLE_NAME, col_name)
    datetime_first = datetime.strptime(first_val, '%Y-%m')
    datetime_last = datetime.strptime(last_val, '%Y-%m')

    _, query_result = dbms.query(query_str)
    result = []
    for row in query_result:
        if row[0] not in IGNORE_VALS and (datetime_first <= datetime.strptime(row[0], '%Y-%m') <= datetime_last):
            result.append(list(row))
    result.sort(key=lambda a: a[0])
    return result
    pass


def _xy_data(dbms, col_name):
    """
    @param dbms: <db> dbms object
    @param col_name: <str> col name
    @return: <json> data
    """
    query_str = """select {}, count(*) as count from {} group by {}""".format(col_name, TABLE_NAME, col_name)
    _, query_result = dbms.query(query_str)
    result = defaultdict(list)
    for row in query_result:
        if row[0] not in IGNORE_VALS:
            result['yData'].append(row[0])
            result['xData'].append(row[1])
    return result
    pass


if __name__ == '__main__':
    application.run(debug=True, host='localhost', port=5001)