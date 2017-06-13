from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
)
from models.fuckzb_requests import Fuckzb

main = Blueprint('fuckzb',__name__)

f1 = Fuckzb()

@main.route('/')
def index():
    f1.yzm()
    return render_template('fuckzb_index.html')


@main.route('/getlist')
def getlist():
    name = request.get('name')
    pwd = request.get('pwd')
    yzm = request.get('yzm')
    f1.log(name, pwd, yzm)
    l = f1.get_zblist()
    return render_template('add_zb.html', l = l)