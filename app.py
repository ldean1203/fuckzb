from flask import Flask, render_template, redirect, url_for, request
import xlrd
import sys
import os
from routes.fuckzb import bpzb



app = Flask(__name__)
app.register_blueprint(bpzb, url_prefix='/fuckzb')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

