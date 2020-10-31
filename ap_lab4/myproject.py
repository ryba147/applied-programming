from flask import Flask
from flask import redirect, url_for

application = Flask(__name__)


@application.route('/')
def index():
    return redirect(url_for('hello_world'))


@application.route('/api/v1/hello-world-3')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    application.run()
