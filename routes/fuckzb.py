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


@main.route('/')
def index():
    Fuckzb.yzm()
    return render_template('fuckzb_index.html')