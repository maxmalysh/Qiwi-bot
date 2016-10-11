#!/usr/local/bin/python.exe
from flask import Flask
import browser
app = Flask(__name__)


@app.route('/<login>/<password>')
def check(login, password):
    if(browser.is_user_exists(login, password)):
        return 'valid'
    else:
        return 'invalid'


@app.route('/<login>/<password>/<type>/<req>/<sum>')
def send_money(login, password, type, req, sum):
    try:
        if(browser.transfer(login, password, type, req, sum)):
            return 'success'
        else:
            return 'fail'
    except Exception:
        return 'captcha'


if __name__ == '__main__':
    app.run()
