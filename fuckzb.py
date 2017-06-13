from flask import Flask, template_rendered, url_for, request

app = Flask(__name__)
@app.route('/fuckzb')
def index():
    return template_rendered('fuckzb_index.html')