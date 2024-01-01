from model.twit import Twit
from flask import Flask, jsonify, request
import json

twits = []
app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().defaul(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/twit', methods=['POST'])
def create_twit():
    twit_json = request.get_json()
    twit = Twit(twit_json['body'], twit_json['author'])
    twits.append(twit)
    return jsonify({'response': 'succes'})


@app.route('/twit', methods=['GET'])
def read_twit():
    return jsonify({'twits': twits})


if __name__ == '__main__':
    app.run(debug=True)
