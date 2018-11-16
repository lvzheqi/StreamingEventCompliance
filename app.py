from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/compliance-checker', methods=['POST'])
def register():
    event = request.json
    print('case_id: ', event['case_id'])
    print('activity: ', event['activity'])
    return 'deviation'


if __name__ == '__main__':
    app.run()
