import requests
import json

HOST = "http://127.0.0.1:5000"

def register(username: str, password: str) -> str | bool:
    data = {"username": username, "password": password}
    response = requests.get(HOST + "/register", json=data).json()
    return response


def login(username: str, password: str) -> str | bool:
    data = {"username": username, "password": password}
    response = requests.get(HOST + "/login", json=data).json()
    return response


def get_info(session_id: str) -> dict:
    response = requests.get(HOST + "/info", json=session_id).json()
    return response


def leaderboard() -> list:
    response = requests.get(HOST + "/leaderboard").json()
    return response


def end_session(session_id: str):
    requests.get(HOST + "/exit", json=session_id)


def play(guess: int, stake: int, session_id: str):
    data = {"session_id": session_id, "stake": stake, "guess": guess}
    response = requests.get(HOST + "/game", json=data).json()
    return response


def registration_process():
    while True:
        print("Username and password must consist of latin letters and numbers only.")
        username = input("Username: ")
        password = input("Password: ")
        session_id = register(username, password)
        if not session_id:
            print("Wrong name/password, or name already taken.")
            print()
        else:
            return session_id


def logging_in_process():
    while True:
        username = input("Username: ")
        password = input("Password: ")
        session_id = login(username, password)
        if not session_id:
            print("Wrong name/password.")
            print()
        else:
            return session_id


def game_process(session_id):
    score = get_info(session_id)["score"]
    while True:
        print("Enter your stake. (50<=, <=your score)")
        try:
            stake = int(input())
        
        except ValueError:
            print("Wrong input.")
            print()
            continue

        if stake >= 50 and stake <= score:
           break 
    print()

    while True:
        print("Take a guess. Enter 1, 2 or 3.")
        try:
            guess = int(input())
        
        except ValueError:
            print("Wrong input")
            print()
            continue
        
        if guess in [1,2,3]:
            break
    print()

    if play(guess, stake, session_id):
        print("You won.")
    else:
        print("You lost.")


def display_player_info(session_id):
    user = get_info(session_id)
    print(user["username"], user["score"])


def display_leaderboard(_):
    leaders = leaderboard()
    for i in leaders:
        print(i["username"], i["score"])


actions1 = {
        "reg": registration_process,
        "log": logging_in_process
}

actions2 = {
        "p": game_process,
        "i": display_player_info,
        "l": display_leaderboard
} 


def main():
    while True:
        print("To register, enter 'reg'.")
        print("To log in. enter 'log'.")
        resp = input().lower()

        try:
            session_id = actions1[resp]()
            break

        except KeyError:
            print("Wrong input.")
            print()

    print()

    while True:
        print("To play the game, enter 'p'.")
        print("To view leaderboard, enter 'l'.")
        print("To view account info, enter 'i'.")
        print("To exit, enter 'e'.")
        resp = input().lower()

        try:
            actions2[resp](session_id)
            print()
        except KeyError:
            if resp == "e":
                end_session(session_id)
                break
            else:
                print("Wrong input.")

try:
    main()

except KeyboardInterrupt:
    try:
        end_session(session_id)
    except Exception as e:
        print(e)

except Exception as e:
    print(e)
    try:
        end_session(session_id)
    except Exception as e:
        print(e)
