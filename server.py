import uuid, json
from flask import Flask

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


    def change_score(self, session_id: str, score_change: int) -> bool:
        account = self.get_account(self.get_username(session_id))

        if account is None:
            return False

        else:
            account["score"] += score_change
            self.update_data()
            return True
