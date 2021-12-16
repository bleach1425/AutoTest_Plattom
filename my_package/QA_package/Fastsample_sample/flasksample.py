from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Wellcome to Flask"

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)