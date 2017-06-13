from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
)

main = Blueprint('fuckzb',__name__)


@main.route('/')
def index():
    print('adfasdfasdfasfd-------------')
    return render_template('fuckzb_index.html')