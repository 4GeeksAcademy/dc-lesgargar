from flask import Blueprint, request, jsonify
from models import User, db

users_bp = Blueprint("users", __name__ , url_prefix="/api/users") 


@users_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.json

    if not data:
        return jsonify({"error": "Missing body"}), 400

    user = User(
        email=data["email"],
        name=data["name"],
        password=data["password"],
        is_active=True,
        role=data.get("role", "customer")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201



@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.serialize()), 200
