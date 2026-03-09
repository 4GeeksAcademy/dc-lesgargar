from flask import Blueprint, request, jsonify
from models import User, db, Profile
from utilss.auth import login_required
from werkzeug.security import generate_password_hash, check_password_hash


users_bp = Blueprint("users", __name__ , url_prefix="/users") 



#@users_bp.route("/", methods=["GET"])
#def get_users():
#    users = User.query.all()
#    return jsonify([u.serialize() for u in users]), 200 


@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.json

    if not data:
        return jsonify({"error": "Missing body"}), 400
    
    email = data.get("email", "").strip()
    name = data.get("name", "").strip()
    password = data.get("password", "").strip()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if not password:
        return jsonify({"error": "Password is required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400


    user = User(
        email=data["email"],
        name=data["name"],
        password=generate_password_hash(password),
        is_active=True,
        role="customer"
    )

    db.session.add(user)

#flush is to save info temp. and it allows to use user.id before the commit 
    db.session.flush()

    profile = Profile(user=user)

    db.session.add(profile)

    db.session.commit()

    return jsonify(user.serialize()), 201



@users_bp.route("/me", methods=["GET"])
@login_required
def get_user(user):
    return jsonify(user.serialize()), 200

#editar user 
@users_bp.route("/me", methods=["PATCH"])
@login_required
def update_user(user):
    data = request.json

    if "name" in data:
        if not data["name"].strip():
            return jsonify({"msg":"Name cannot be empty"})
        user.name = data["name"].strip()
    if "email" in data:
        if not data["email"].strip():
            return jsonify({"msg":"Email cannot be empty"}), 400
        #validates if user exists
        existing = User.query.filter_by(email=data["email"]).first()

        if existing and existing.id != user.id:
            return jsonify({"msg": "Email already in use"}), 400
        
        user.email = data["email"].strip()

    if "password" in data:
        if not data["password"].strip():
            return jsonify({"msg": "Password cannot be empty"}), 400
            
        user.password = generate_password_hash(data["password"])
    
    db.session.commit()

    return jsonify(user.serialize()),200




