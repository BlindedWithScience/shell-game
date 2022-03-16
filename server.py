import uuid
import json
from flask import Flask, request


class DataManager:
    def __init__(self):
        self.accounts = self.read_data()
        self.sessions = []

    def read_data(self) -> list:
        try:
            with open("accounts.json", "r") as file:
                return json.loads(file.read())

        except FileNotFoundError:
            return []

    def update_data(self) -> bool:
        try:
            with open("accounts.json", "w") as file:
                file.write(json.dumps(self.accounts, indent=4))
            return True

        except Exception:
            return False

    def get_account(self, username: str) -> dict | None:
        if username is None:
            return None

        for item in self.accounts:
            if item["username"] == username:
                return item

    def register(self, username: str, password: str) -> str | None:
        if not (username.isalnum() and password.isalnum()):
            return None

        if self.get_account(username) is not None:
            return None

        self.accounts.append(
            {
                "username": username,
                "password": password,
                "score": 500
            }
        )

        self.update_data()

        session_id = str(uuid.uuid4())
        self.sessions.append(
            {
                "session_id": session_id,
                "username": username
            }
        )

        return session_id

    def login(self, username: str, password: str) -> str | None:
        account = self.get_account(username)
        if account["password"] == password:
            session_id = str(uuid.uuid4())

            self.sessions.append(
                {
                    "session_id": session_id,
                    "username": username
                }
            )

            return session_id

        return None

    def get_username(self, session_id: str) -> str | None:
        for item in self.sessions:
            if item["session_id"] == session_id:
                return item["username"]

        return None

    def get_info(self, session_id: str) -> dict | None:
        account = self.get_account(self.get_username(session_id))

        if account is None:
            return None

        return {"username": account["username"], "score": account["score"]}

    def change_score(self, session_id: str, score_change: int) -> bool:
        account = self.get_account(self.get_username(session_id))

        if account is None:
            return False

        else:
            account["score"] += score_change
            self.update_data()
            return True

    def leaderboard(self, n: int) -> list:
        self.accounts.sort(reverse=True, key=lambda a: a["score"])
        array = self.accounts
        return [{"username": array[i]["username"], "score": array[i]["score"]} for i in range(n)]

    def exit(self, session_id: str):
        for i in range(len(self.sessions)):
            if self.sessions[i]["session_id"] == session_id:
                self.sessions.pop(i)


manager = DataManager()
app = Flask(__name__)


@app.route("/register")
def register():
    data = request.get_json()
    session_id = manager.register(data["username"], data["password"])
    return json.dumps({"result": session_id is not None, "session_id": session_id})


@app.route("/login")
def login():
    data = request.get_json()
    session_id = manager.login(data["username"], data["password"])
    return json.dumps({"result": session_id is not None, "session_id": session_id})


@app.route("/game")
def game():
    data = request.get_json()
    if data["guess"] != rand.randint(1, 3):
        data["stake"] *= -1
    return json.dumps(manager.change_score(data["session_id"], data["stake"]))


@app.route("/info")
def info():
    session_id = request.get_json()
    info = manager.get_info(session_id)
    return json.dumps({"result": info is not None, "info": info})


@app.route("/leaderboard")
def leaderboard():
    return json.dumps(manager.leaderboard(10))


@app.route("/exit")
def exit():
    session_id = request.get_json()
    manager.exit(session_id)
