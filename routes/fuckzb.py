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

@main.route("/")
def index():
    f1.yzm()
    return render_template('fuckzb_index.html')

@main.route("/login", methods=["POST"])
def login():
    name = request.form.get('userid', '')
    pwd = request.form.get('pwd', '')
    yzm = request.form.get('yzm', '')
    checked = f1.log(name, pwd, yzm)
    print('checked is ----------', checked)
    if checked == None or checked[0] == 1:
        return redirect(url_for('.getlist'))
    else:
        print('checked is ----------', checked)
        return redirect(url_for('.index'))

@main.route("/getlist")
def getlist():
    l = f1.get_zblist()
    return render_template('add_zb.html', l=l)

@main.route("/add", methods=["POST"])
def add():
    date = request.form.get('date','')
    content = request.form.get('content','')
    f1.add_zb_detail(date, content)
    return redirect(url_for('.getlist'))