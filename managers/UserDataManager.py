import json
import uuid

class UserDataManager:
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

    def get_account(self, username: str) -> dict | bool:
        if not username:
            return False

        for item in self.accounts:
            if item["username"] == username:
                return item

    def register(self, username: str, password: str) -> str | bool:
        if not (username.isalnum() and password.isalnum()):
            return False

        if self.get_account(username):
            return False

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

    def login(self, username: str, password: str) -> str | bool:
        account = self.get_account(username)
        
        if not account:
            return False

        if account["password"] == password:
            session_id = str(uuid.uuid4())

            self.sessions.append(
                {
                    "session_id": session_id,
                    "username": username
                }
            )

            return session_id
        
        else:
            return False

    def get_username(self, session_id: str) -> str | bool:
        for item in self.sessions:
            if item["session_id"] == session_id:
                return item["username"]

        return False

    def get_info(self, session_id: str) -> dict | bool:
        account = self.get_account(self.get_username(session_id))

        if not account:
            return False

        return {"username": account["username"], "score": account["score"]}

    def change_score(self, session_id: str, score_change: int) -> bool:
        account = self.get_account(self.get_username(session_id))

        if not account:
            return False

        else:
            account["score"] += score_change
            self.update_data()
            return True

    def leaderboard(self, n: int) -> list:
        self.accounts.sort(reverse=True, key=lambda a: a["score"])
        array = self.accounts
        return [{"username": array[i]["username"], "score": array[i]["score"]} for i in range(min(len(array), n))]

    def end_session(self, session_id: str):
        for i in range(len(self.sessions)):
            if self.sessions[i]["session_id"] == session_id:
                self.sessions.pop(i)


