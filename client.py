import requests
import json

HOST = "http://127.0.0.1:5000"

def register(username: str, password: str) -> str | None:
    data = {"username": username, "password": password}
    response = requests.get(HOST + "/register", data=json.dumps(data)).text
    return response


def login(username: str, password: str) -> str | None:
    data = {"username": username, "password": password}
    response = requests.post(HOST + "/login", data=json.dumps(data)).text
    print(response)
    return response


def get_info(session_id: str) -> dict:
    response = json.loads(requests.get(HOST + "/info", data=session_id).text)
    return response


def leaderboard() -> list:
    response = json.loads(requests.get(HOST + "/leaderboard").text)
    return response


def end_session(session_id: str):
    requests.get(HOST + "/exit", data=session_id)


def play(guess: int, stake: int, session_id: str):
    sdata = json.dumps({"session_id": session_id, "stake": stake, "guess": guess})
    #response = json.loads(requests.get(HOST + "/game", data=json.dumps(data)).text)
    response = json.loads(requests.post(HOST + "/game", data=sdata).text)
    print(response)
    return response


def main():
    while True:
        print("To register, enter 'r'.")
        print("To log in. enter 'l'.")
        resp = input().lower()

        if resp != "r" and resp != "l":
            print("Wrong input.")
            print()
            continue

        break

    print()

    if resp == "r":
        while True:
            print("Username and password must consist of latin letters and numbers only.")
            username = input("Username: ")
            password = input("Password: ")
            session_id = register(username, password)
            if session_id is None:
                print("Wrong name/password, or name already taken.")
                print()
            else:
                break

    if resp == "l":
        while True:
            username = input("Username: ")
            password = input("Password: ")
            session_id = login(username, password)
            if session_id is None:
                print("Wrong name/password.")
                print()
            else:
                break
    print()

    while True:
        print("To play the game, enter 'p'.")
        print("To view leaderboard, enter 'l'.")
        print("To view account info, enter 'i'.")
        print("To exit, enter 'e'.")
        resp = input().lower()

        if resp == "p":
            score = get_info(session_id)["score"]
            while True:
                print("Enter your stake. (50<=, <=your score)")
                try:
                    stake = int(input())
                
                except Exception:
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
                
                except Exception:
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

        elif resp == "l":
            leaders = leaderboard()
            for i in leaders:
                print(i["username"], i["score"])
        
        elif resp == "i":
            user = get_info(session_id)
            print(user["username"], user["score"])

        elif resp == "e":
            end_session(session_id)
            break

        else:
            print("Wrong input.")

main()
"""
try:
    main()

except KeyboardInterrupt:
    try:
        end_session(session_id)
    except Exception:
        pass

except Exception as e:
    print(e)
    try:
        end_session(session_id)
    except Exception:
        pass
"""
