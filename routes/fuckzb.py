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
    l = f1.get_addlist()
    return render_template('add_zb.html', l=l)

@main.route("/delete/<int:del_id>", methods=["POST"])
def delete():
    return redirect(url_for('.getlist'))

@main.route("/add", methods=["POST"])
def add():
    date = request.form.get('date','')
    content = request.form.get('content','')
    start_time = request.form.get('start_time','')
    end_time = request.form.get('end_time','')
    f1.add_zb_detail(date, start_time, end_time, content)
    return redirect(url_for('.getlist'))