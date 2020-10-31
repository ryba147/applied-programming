from flask import Flask
from flask import render_template, redirect, url_for

application = Flask(__name__)
v = 3


@application.route('/')
def index():
    return redirect(url_for('hello_world', url_v=v))


@application.route('/api/v1/hello-world-<int:url_v>')  # route() decorator tells Flask what URL should trigger our function
def hello_world(url_v):
    return render_template('hello.html', var=url_v)  # or return 'Hello World!'


if __name__ == '__main__':
    application.run(host='0.0.0.0')
