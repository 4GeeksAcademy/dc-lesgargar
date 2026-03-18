#Role verification

from functools import wraps
from flask import request, jsonify
from models import User, db
from utilss.jwt import decode_token


def get_current_user():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]
        data = decode_token(token)
        user = db.session.get(User, data["user_id"])
        return user
    except:
        return None



#Verified users / permissions
def login_required(funct):
    @wraps(funct)

    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({"error":"Unauthorized user"}), 401
        
        return funct(user, *args, **kwargs )
    

    return wrapper


#Ver¡fy Admin user
def admin_required(funct):
    @wraps(funct)

    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        if user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
    
        return funct(user, *args, **kwargs)

    return wrapper
    
#optional
def login_optional(funct):
    @wraps(funct)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return funct(None, *args, **kwargs)

        if not auth:
            return funct(None, *args, **kwargs)
        try:
            token = auth.split(" ")[1]
            payload = decode_token(token)

            user = User.query.get(payload["user_id"])
            return funct(user, *args, **kwargs)
        
        except Exception:
            return funct(None, *args, **kwargs)
    return wrapper
