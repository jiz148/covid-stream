import base64
from io import BytesIO

import flask
from flask import Flask, jsonify, request
from flask_cors import CORS


application = Flask(__name__)
# CORS
CORS(application)
# run producer


@application.route('/', methods=['GET', 'POST'])
def query():
    """
    post: receive json and add into database
    @return:
    """
    if request.method == 'POST':
        _add_to_db(request.form)
    else:
        _get_data_from_query(request.form)
    pass


def _add_to_db(case_data):
    """
    @param case_data: <dict>
    @return: <boolean> success
    """
    pass


def _get_data_from_query(query_data):
    """
    @param query_data: <dict>
    @return: <boolean> success
    """
    pass


if __name__ == '__main__':
    application.run()