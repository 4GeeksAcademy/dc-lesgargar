from models import db, User, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from utilss.validators import validate_email_format, validate_password_strength

def register_user(data):

    email = data.get("email", "").strip()
    name = data.get("name", "").strip()
    password = data.get("password", "").strip()

    if not email or not validate_email_format(email):
        raise ValueError("Invalid email format")

    if not validate_password_strength(password):
        raise ValueError("Password too weak")

    if User.query.filter_by(email=email).first():
        raise ValueError("Email already registered")

    user = User(
        email=email,
        name=name,
        password=generate_password_hash(password),
        role="customer"
    )

    db.session.add(user)
    db.session.commit()

    return user


def authenticate_user(email, password):

    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not check_password_hash(user.password, password):
        return None

    return user
