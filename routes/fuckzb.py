from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
)
import time
from models.fuckzb_requests import Fuckzb

main = Blueprint('fuckzb',__name__)

f1 = Fuckzb()

@main.route("/")
def index():
    ip = request.remote_addr
    f1.yzm(ip)
    return render_template('fuckzb_index.html', user_ip = ip)

@main.route("/login", methods=["POST"])
def login():
    name = request.form.get('userid', '')
    pwd = request.form.get('pwd', '')
    yzm = request.form.get('yzm', '')
    checked = f1.log(name, pwd, yzm)
    if checked == None or checked[0] == 1:
        return redirect(url_for('.getlist'))
    else:
        return redirect(url_for('.index'))

@main.route("/getlist")
def getlist():
    l,uname = f1.get_addlist()
    return render_template('add_zb.html', l=l, uname = uname)

@main.route("/delete/<del_id>", methods=["POST", "GET"])
def delete(del_id):
    f1.delete_zb(del_id)
    return redirect(url_for('.getlist'))

@main.route("/add", methods=["POST"])
def add():
    date = request.form.get('date','')
    content = request.form.get('content','')
    start_time = request.form.get('start_time','')
    end_time = request.form.get('end_time','')
    f1.add_zb_detail(date, start_time, end_time, content)
    return redirect(url_for('.getlist'))

@main.route("/dayadd", methods=["POST"])
def dayadd():
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    content = request.form.get('content1','')
    start_time = '9:00'
    end_time = '18:00'
    f1.add_zb_detail(date, start_time, end_time, content)
    return redirect(url_for('.getlist'))