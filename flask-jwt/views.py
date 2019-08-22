# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:50:51 2019

@author: mdamelio
"""

from run import app
from flask import jsonify

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})