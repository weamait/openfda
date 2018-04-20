from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/clase")
def hello():
    limite = request.args.get('limit')
    return "Hello World!"+limite


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
