#!flask/bin/python

from flask import Flask, json, jsonify, Response, request

app = Flask(__name__)
users = []

class User(object):
    def __init__(self, name):
        self.name = name
        self.tasks = []

class Task(object):
    def __init__(self, id, name, state):
        self.id = id
        self.name = name
        self.state = state

def findUser(name):
    i = 0
    user = None
    while i < len(users) and user == None:
        if (users[i].name == name):
            user = users[i]
        i+=1

    return user

def findTask(user, taskId):
    i = 0
    task = None
    tasks = user.tasks
    while i < len(tasks) and task == None:
        if (int(tasks[i].id) == int(taskId)):
            task = tasks[i]
        i+=1

    return task

@app.route('/todo/task/<userName>', methods=['GET'])
def tasks(userName):

    taskSearizable = None
    user = findUser(userName)
    if (user != None):
        taskSearizable = json.dumps([task.__dict__ for task in user.tasks])
    else:
        return Response(status=204)

    return Response(taskSearizable,
                    status=200,
                    mimetype='application/json')

@app.route('/todo/task/<userName>/<taskId>', methods=['GET'])
def task(userName, taskId):

    taskSearizable = None
    user = findUser(userName)
    if (user != None):
        task = findTask(user, taskId)
        if (task != None):
            taskSearizable = json.dumps(task.__dict__)
        else:
            return Response(status=204)
    else:
        return Response(status=204)

    return Response(taskSearizable,
                    status=200,
                    mimetype='application/json')

@app.route('/todo/task', methods=['POST'])
def addTask():

    requestBody = request.get_json()
    
    userName = requestBody["name"]
    user = findUser(userName)
    if user == None:
        user = User(userName)
        users.append(user)

    tasks = user.tasks
    taskId = 0
    if (len(tasks) <= 0):
        taskId = 1
    else:
        taskId = tasks[len(tasks) - 1].id + 1
    tasks.append(Task(taskId, requestBody["task"]["name"], requestBody["task"]["state"]))
    return Response(status=200)

@app.route('/todo/task/<taskId>', methods=['PUT'])
def editTask(taskId):

    requestBody = request.get_json()

    user = findUser(requestBody["name"])
    if (user != None):
        task = findTask(user, taskId)
        if (task != None):
            task.name = requestBody["task"]["name"]
            task.state = requestBody["task"]["state"]

    return Response(status=200)

@app.route('/todo/task/<userName>/<taskId>', methods=['PUT'])
def deleteTask(userName, taskId):

    requestBody = request.get_json()

    user = findUser(userName)
    if (user != None):
        task = findTask(user, taskId)
        user.tasks.remove(task)

    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')