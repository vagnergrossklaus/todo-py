#!flask/bin/python

from flask import Flask, json, jsonify, Response, request

app = Flask(__name__)
users = []

class User(object):
    def __init__(self, name):
        self.name = name
        self.tasks = []

class Task(object):
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status

@app.route('/todo/tasks/<user_name>', methods=['GET'])
def get_tasks(user_name):

    task1 = Task(1, "teste", 1)

    taskSearizable = json.dumps(task1.__dict__)
    return Response(taskSearizable,
                    status=200,
                    mimetype='application/json')

@app.route('/todo/task', methods=['POST'])
def post_task():

    requestBody = request.get_json()
    
    user = None
    userName = requestBody["name"]
    indexUser = users.index(userName)
    if (indexUser >= 0):
        user = User(userName)
        users.append(user)
    else:
        user = users[indexUser]

    print(request.get_json())

    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')