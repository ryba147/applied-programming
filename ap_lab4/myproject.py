from flask import Flask
from flask import render_template, redirect, url_for

application = Flask(__name__)


@application.route('/')
def index():
    return redirect(url_for('hello_world'))


@application.route('/api/v1/hello-world-3')  # route() decorator tells Flask what URL should trigger our function
def hello_world():
    return render_template('hello.html')  # or return 'Hello World!'


if __name__ == '__main__':
    application.run(host='0.0.0.0')
