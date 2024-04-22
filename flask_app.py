
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,send_from_directory

app = Flask(__name__)

@app.route('/')
def hello_world():
    return send_from_directory('','result.xml')

