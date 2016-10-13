#!D:/Users/gorno/AppData/Local/Programs/Python/Python35-32/python.exe
from flask import Flask
import browser
app = Flask(__name__)


@app.route('/<login>/<password>/<action>')
def check(login, password, action):

    if action == 'check':
        if browser.is_user_exists(login, password):
            return 'valid'.encode('utf-8')
        else:
            return 'invalid'.encode('utf-8')
    elif action == 'balance':
        return browser.get_balance(login, password)

    return 'captcha'.encode('utf-8')


@app.route('/<login>/<password>/<type>/<req>/<sum>')
def send_money(login, password, type, req, sum):
    try:
        if browser.transfer(login, password, type, req, sum):
            return 'success'.encode('utf-8')
        else:
            return 'fail'.encode('utf-8')
    except Exception:
        return 'captcha'.encode('utf-8')


if __name__ == '__main__':
    app.run()
