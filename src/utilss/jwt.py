import jwt
import datetime
import os

SECRET_KEY = os.getenv("FLASK_APP_KEY")

def generate_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=24)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
