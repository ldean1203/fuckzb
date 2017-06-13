from flask import Flask, template_rendered, url_for, request, Blueprint

bpzb = Blueprint('fuckzb','__name__')

@bpzb.route('/')
def index():
    return template_rendered('fuckzb_index.html')