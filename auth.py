USERS = {
    "adenilson": {
        "password": "1234",
        "display_name": "Professor Adenilson",
    },
    "orlando": {
        "password": "1234",
        "display_name": "Professor Orlando",
    },
    "francisco": {
        "password": "1234",
        "display_name": "Professor Francisco",
    },
}


def authenticate(username: str, password: str) -> bool:
    username = (username or "").strip().lower()
    password = (password or "").strip()

    user = USERS.get(username)
    if not user:
        return False

    return user["password"] == password


def get_display_name(username: str) -> str:
    username = (username or "").strip().lower()
    user = USERS.get(username)
    if not user:
        return username
    return user["display_name"]


def user_exists(username: str) -> bool:
    return (username or "").strip().lower() in USERS
