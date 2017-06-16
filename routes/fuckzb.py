from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
    Response,
    session,
    Flask
)
import json
import time,datetime
import os
from models.fuckzb_requests import Fuckzb

main = Blueprint('fuckzb',__name__)

f1 = Fuckzb()


@main.route("/", methods=["GET","POST"])
def index():
    # ip = request.remote_addr
    # ip = json.dumps(request.cookies)
    code = f1.yzm()
    print('session is ----',session)
    return render_template('fuckzb_index.html', code = code)

@main.route("/login", methods=["POST"])
def login():
    name = request.form.get('userid', '')
    pwd = request.form.get('pwd', '')
    yzm = request.form.get('yzm', '')
    checked = f1.log(name, pwd, yzm)
    session['userid'] = name
    print("from login:",session)
    if checked == None or checked[0] == 1:
        return redirect(url_for('.getaddlist'))
    else:
        flash(checked)
        return redirect(url_for('.index'))

@main.route("/getaddlist")
def getaddlist():
    l = f1.get_addlist()
    print("from getaddlist:",session)
    return render_template('add_zb.html', l=l)

@main.route("/delete/<del_id>", methods=["POST", "GET"])
def delete(del_id):
    f1.delete_zb(del_id)
    print("from delete:",session)
    return redirect(url_for('.getaddlist'))

@main.route("/add", methods=["POST"])
def add():
    date = request.form.get('date','')
    content = request.form.get('content','')
    start_time = request.form.get('start_time','')
    end_time = request.form.get('end_time','')
    status = f1.add_zb(date)
    if status[0] == 0:
        flash(status[2:-1])
    s2 = f1.add_zb_detail(date, start_time, end_time, content, status[2:-1])
    if s2 != None:
        flash(s2)
    print("from add:",session)
    return redirect(url_for('.getaddlist'))

@main.route("/dayadd", methods=["POST"])
def dayadd():
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    content = request.form.get('content1','')
    start_time = '9:00'
    end_time = '18:00'
    status = f1.add_zb(date)
    if status[0] == 0:
        flash(status[2:-1])
    s2 = f1.add_zb_detail(date, start_time, end_time, content, status[2:-1])
    if s2 != None:
        flash(s2)
    print("from add:",session)
    return redirect(url_for('.getaddlist'))

@main.route("/getlist", methods=["GET","POST"])
def getlist():
    l = f1.get_zblist()
    print("from getlist:",session)
    return render_template('add_zb.html',l = l)

@main.route("/fivedays", methods=["POST"])
def fivedays():
    today = datetime.date.today()
    content = '驻场'
    start_time = '9:00'
    end_time = '18:00'
    for i in range(3,8):
        sunday = today + datetime.timedelta(6 - today.weekday() + 1) - datetime.timedelta(i)
        date = sunday.strftime("%Y-%m-%d")

        status = f1.add_zb(date)
        if status[0] == 0:
            flash(status[2:-1])
        s2 = f1.add_zb_detail(date, start_time, end_time, content, status[2:-1])
        if s2 != None:
            flash(s2)
    print("from fivedays:",session)
    return redirect(url_for('.getaddlist'))