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


@main.route("/getlist",  methods=["POST"])
def getlist():
    name = request.form.get('userid', '')
    pwd = request.form.get('pwd', '')
    yzm = request.form.get('yzm', '')
    checked = f1.log(name, pwd, yzm)
    if checked == None:
        l = f1.get_zblist()
        return render_template('add_zb.html')
    else:
        print(checked)
        return redirect(url_for('.index'))