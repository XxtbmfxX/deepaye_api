def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "password": user["password"],
            "disabled": user["disabled"]
            }


def users_schema(users) -> list:
    return [user_schema(user) for user in users]


def user_db_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "disabled": user["disabled"]
            }


def users_from_db_schema(users) -> list:
    return [user_db_schema(user) for user in users]
