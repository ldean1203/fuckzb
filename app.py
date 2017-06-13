from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import Blueprint

from routes.fuckzb import main as fuckzb_routes



app = Flask(__name__)
app.register_blueprint(fuckzb_routes, url_prefix='/fuckzb')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

