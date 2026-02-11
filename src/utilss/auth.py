#Here wew verify the rol 

from functools import wraps
from flask import request, jsonify
from models import User, db

#Get current user:  -----------------se va a cambiar por JTW-----------------------

def get_current_user():
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return None
    
    return db.session.get(User, int(user_id))



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
    
