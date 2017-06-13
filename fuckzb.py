from flask import Flask, template_rendered, url_for, request, Blueprint

fuckzb = Blueprint('fuckzb','__name__')

@fuckzb.route('/')
def index():
    return template_rendered('fuckzb_index.html')