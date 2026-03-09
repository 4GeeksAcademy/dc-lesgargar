from flask import Blueprint, request, jsonify
from services.user_service import register_user, authenticate_user
from utilss.jwt import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

#Register user 

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        user = register_user(request.json)
        return jsonify({"msg":"User created"}),201
    except ValueError as err:
        return jsonify({"error":str(err)}), 400
    
@auth_bp.route("/login", methods = ["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = authenticate_user(email, password)

    if not user:
        return jsonify({"msg":"Invalid login"}), 401
    
    token = generate_token(user)

    return jsonify({"token": token})

