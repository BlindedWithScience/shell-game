import json
import random
from managers.UserDataManager import UserDataManager
from flask import Flask, request, make_response

manager = UserDataManager()
app = Flask(__name__)

@app.route("/register")
def register():
    data = request.get_json()
    session_id = json.dumps(manager.register(data["username"], data["password"]))
    response = make_response(session_id)
    response.content_type = "application/json"
    return response


@app.route("/login")
def login():
    data = request.get_json()
    session_id = json.dumps(manager.login(data["username"], data["password"]))
    response = make_response(session_id)
    response.content_type = "application/json"
    return response


@app.route("/game")
def game():
    data = request.get_json()
    result = data["guess"] != random.randint(1, 3)
    if not result:
        data["stake"] *= -1
    manager.change_score(data["session_id"], data["stake"])
    response = make_response(json.dumps(result))
    response.content_type = "application/json"
    return response


@app.route("/info")
def info():
    session_id = request.get_json()
    info = json.dumps(manager.get_info(session_id))
    response = make_response(info)
    response.content_type = "application/json"
    return response


@app.route("/leaderboard")
def leaderboard():
    data = json.dumps(manager.leaderboard(10))
    response = make_response(data)
    response.content_type = "application/json"
    return response


@app.route("/exit")
def end_session():
    session_id = request.get_json()
    manager.end_session(session_id)
    return make_response()

if __name__ == "__main__":
    app.run()
