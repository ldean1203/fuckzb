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
    code = f1.yzm()
    return render_template('fuckzb_index.html', code = code)

@main.route("/login", methods=["POST"])
def login():
    name = request.form.get('userid', '')
    pwd = request.form.get('pwd', '')
    yzm = request.form.get('yzm', '')
    checked = f1.log(name, pwd, yzm)
    session['userid'] = name
    if checked == None or checked[0] == 1:
        return redirect(url_for('.getaddlist'))
    else:
        flash(checked)
        return redirect(url_for('.index'))

@main.route("/getaddlist")
def getaddlist():
    l = f1.get_addlist()
    return render_template('add_zb.html', l=l)

@main.route("/delete/<del_id>", methods=["POST", "GET"])
def delete(del_id):
    f1.delete_zb(del_id)
    return redirect(url_for('.getaddlist'))

@main.route("/add", methods=["POST"])
def add():
    overwork_hour = ''
    overwork = 2
    work_type = '211'
    date = request.form.get('date','')
    content = request.form.get('content','')
    start_time = request.form.get('start_time','')
    end_time = request.form.get('end_time','')
    work_type = request.form.get('rest','')
    if end_time == '24:00':
        end_time = '23:59'
    status = f1.add_zb(date)
    if status[0] == '0':
        flash(status[2:-1])
        return redirect(url_for('.getaddlist'))
    if int(end_time[:-3]) > 18:
        overwork_hour = int(end_time[:-3]) - 18
        overwork = 1
    s2 = f1.add_zb_detail(date, start_time, end_time, content, status[2:-1], overwork, overwork_hour, work_type)
    if s2 != None:
        flash(s2)
    return redirect(url_for('.getaddlist'))

@main.route("/dayadd", methods=["POST"])
def dayadd():
    overwork_hour = ''
    overwork = 2
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    content = request.form.get('content1','')
    start_time = '9:00'
    end_time = request.form.get('end_time','')
    work_type = request.form.get('rest','')
    status = f1.add_zb(date)
    if status[0] == '0':
        flash(status[2:-1])
    if end_time == '24:00':
        end_time = '23:59'
    if int(end_time[:-3]) > 18:
        overwork_hour = int(end_time[:-3]) - 18
        overwork = 1
    s2 = f1.add_zb_detail(date, start_time, end_time, content, status[2:-1], overwork, overwork_hour,work_type)
    if s2 != None:
        flash(s2)
    return redirect(url_for('.getaddlist'))

@main.route("/getlist", methods=["GET","POST"])
def getlist():
    l = f1.get_zblist()
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
        if status[0] == '0':
            flash(status[2:-1])
        s2 = f1.add_zb_detail(date, start_time, end_time, content, status[2:-1])
        if s2 != None:
            flash(s2)
    return redirect(url_for('.getaddlist'))

@main.route("/addmultidetail", methods=["POST"])
def addmultidetail():
    overwork_hour = ''
    overwork = 2
    date = request.form.get('date1','')
    content1 = request.form.get('content1','')
    start_time1 = request.form.get('start_time1','')
    end_time1 = request.form.get('end_time1','')
    content2 = request.form.get('content2','')
    start_time2 = request.form.get('start_time2','')
    end_time2 = request.form.get('end_time2','')
    jb = request.form.get('jb','')
    status = f1.add_zb(date)
    if status[0] == '0':
        flash(status[2:-1])
    if jb == 'on':
        overwork_hour = int(end_time1[:-3])
        overwork = 1
    s1 = f1.add_zb_detail(date, start_time1, end_time1, content1, status[2:-1], overwork, overwork_hour)
    if s1 != None:
        flash(s1)
    if end_time2 == '24:00':
        end_time2 = '23:59'
    if int(end_time2[:-3]) > 18:
        overwork_hour = int(end_time2[:-3]) - 18
        overwork = 1
    else:
        overwork_hour = ''
        overwork = 2
    s2 = f1.add_zb_detail(date, start_time2, end_time2, content2, status[2:-1], overwork, overwork_hour)
    if s2 != None:
        flash(s2)
    return redirect(url_for('.getaddlist'))