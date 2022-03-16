import requests
import json

HOST = "http://127.0.0.1:5000"

def register(username: str, password: str) -> str | None:
    data = {"username": username, "password": password}
    response = requests.get(HOST + "/register", data=json.dumps(data)).json()
    return response


def login(username: str, password: str) -> str | None:
    data = {"username": username, "password": password}
    response = requests.get(HOST + "/login", data=json.dumps(data)).json()
    return response


def get_info(session_id: str) -> dict:
    response = requests.get(HOST + "/info", data=session_id).json()
    return response


def leaderboard() -> list:
    response = requests.get(HOST + "/leaderboard").json()
    return response


def exit(session_id: str):
    requests.get(HOST + "/exit", data=session_id)


def play(guess: int, stake: int, session_id: str):
    data = {"session_id": session_id, "stake": stake, "guess": guess}
    response = requests.get(HOST + "/game", data=json.dumps(data)).json()
    return response
