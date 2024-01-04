from model.twit import Twit
from model.comment import Comment
from flask import Flask, jsonify, request
import json
import uuid

twits = []
comments = []
app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit) or isinstance(obj, Comment):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().defaul(obj)

app.json_encoder = CustomJSONEncoder
@app.route('/')
def printing(arg):
    return arg

def generate_id(prefix):
    return f'{prefix}_{uuid.uuid4()}'

@app.route("/twit/create", methods=["POST"])
def create_twit_form():
    twit_body = request.form.get("body")
    twit_author = request.form.get("author")
    twit_id = generate_id(prefix='t')
    twit = Twit(body=twit_body, author=twit_author)
    twit = json.dumps(twit, indent=None,
                            ensure_ascii=False,
                            check_circular=False,
                            allow_nan=False,
                            skipkeys=False,
                            sort_keys=False,
                            separators=None,
                            cls=CustomJSONEncoder)
    twit = json.loads(twit)
    twit["twit_id"] = twit_id
    twit = json.dumps(twit)
    twits.append(twit)
    return jsonify({'response': 'success'})

@app.route("/comments/create", methods=["GET","POST"])
def create_comment_form():

    if request.method == 'GET':
        return jsonify({'twits': twits})
    else:
        found_twit = False
        found_twit_id = request.form.get("twit_id")
        for twit in twits:
            twit = json.loads(twit)
            twit_id = twit.get("twit_id")
            if found_twit_id == twit_id:
                found_twit = True
                break

        if found_twit == False:
            return jsonify({'response': 'Fail: twit not found'})
        else:
            comment_body = request.form.get("body")
            comment_author = request.form.get("author")
            comment_id = generate_id(prefix='c')
            comment = Comment(body=comment_body, author=comment_author)
            comment = json.dumps(comment, indent=None,
                              ensure_ascii=False,
                              check_circular=False,
                              allow_nan=False,
                              skipkeys=False,
                              sort_keys=False,
                              separators=None,
                              cls=CustomJSONEncoder)
            comment = json.loads(comment)
            comment["twit_id"] = found_twit_id
            comment["comment_id"] = comment_id
            comment = json.dumps(comment)
            comments.append(comment)
            return jsonify({'response': 'success'})


@app.route("/twit/update", methods=["PUT", "GET"])
def update_twit_form():

    if request.method == 'GET':
        return jsonify({'twits': twits})
    else:
        update_twit_id = request.form.get("twit_id")
        found_update_twit = False
        twit_index = None
        for count in range(len(twits)):
            twit = json.loads(twits[count])
            twit_id = twit.get("twit_id")
            if update_twit_id == twit_id:
                twit_index = count
                found_update_twit = True
                break
        if found_update_twit == False:
            return jsonify({'response': 'Fail: twit not found'})
        else:
            twit = json.loads(twits[twit_index])
            twit['body'] = request.form.get("body")
            twit = json.dumps(twit)
            twits[twit_index] = twit
            return jsonify({'response': 'success'})

@app.route("/comment/update", methods=["PUT", "GET"])
def update_comment_form():

    if request.method == 'GET':
        return jsonify({'comment': comments})
    else:
        update_comment_id = request.form.get("comment_id")
        found_update_comment = False
        comment_index = None
        for count in range(len(comments)):
            comment = json.loads(comments[count])
            comment_id = comment.get("twit_id")
            if update_comment_id == comment_id:
                comment_index = count
                found_update_comment = True
                break
        if found_update_comment == False:
            return jsonify({'response': 'Fail: comment not found'})
        else:
            comment = json.loads(comments[comment_index])
            comment['body'] = request.form.get("body")
            comment = json.dumps(comment)
            comments[comment_index] = comment
            return jsonify({'response': 'success'})

@app.route("/twit/delete", methods=["DELETE", "GET"])
def delete_twit_form():

    if request.method == 'GET':
        return jsonify({'twits': twits})
    else:
        delete_twit_id = request.form.get("twit_id")
        found_delete_twit = False
        twit_index = None
        for count in range(len(twits)):
            twit = json.loads(twits[count])
            twit_id = twit.get("twit_id")
            if delete_twit_id == twit_id:
                found_delete_twit = True
                twit_index = count
                break
        if found_delete_twit == False:
            return jsonify({'response': 'Fail: twit not found'})
        else:
            twits.remove(twits[twit_index])
            return jsonify({'response': 'success'})

@app.route("/comment/delete", methods=["DELETE", "GET"])
def delete_comment_form():

    if request.method == 'GET':
        return jsonify({'comments': comments})
    else:
        delete_comment_id = request.form.get("comment_id")
        found_delete_comment = False
        comment_index = None
        for count in range(len(comments)):
            comment = json.loads(comments[count])
            comment_id = comment.get("comment_id")
            if delete_comment_id == comment_id:
                found_delete_comment = True
                comment_index = count
                break
        if found_delete_comment == False:
            return jsonify({'response': 'Fail: comment not found'})
        else:
            comments.remove(comments[comment_index])
            return jsonify({'response': 'success'})

@app.route('/twit', methods=['GET'])
def read_twits():
    return jsonify({'twits': twits})

@app.route('/comments', methods=['GET'])
def read_comments():
    return jsonify({'comments': comments})


if __name__ == '__main__':
    app.run(debug=True)
