from flask import request, jsonify, Blueprint

from utilss.auth import login_required
from models import db

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods= ["GET"])
@login_required
def get_profile(user):
    profile = user.profile
    if not profile:
        return jsonify({"msg":"profile not found"}),404
    return jsonify(profile.serialize()), 200
    
@profile_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile(user):
    profile = user.profile
    if not profile:
        return jsonify({"msg":"profile not found"}), 404
    
    data = request.json

    profile.phone = data.get("phone")
    profile.street = data.get("street")
    profile.neighborhood = data.get("neighborhood")
    profile.postal_code = data.get("postal_code")
    profile.city = data.get("city")
    profile.country = data.get("country")
    profile.references = data.get("references")

    db.session.commit()

    return jsonify(profile.serialize()),200

@profile_bp.route("/profile", methods=["PATCH"])
@login_required
def edit_profile(user):
    profile = user.profile

    if not profile: 
        return jsonify({"msg":"profile not found"}),404
    
    data = request.json

    profile.phone = data.get("phone", profile.phone)
    profile.street = data.get("street", profile.street)
    profile.neighborhood = data.get("neighborhood", profile.neighborhood)
    profile.postal_code = data.get("postal_code", profile.postal_code)
    profile.city = data.get("city", profile.city)
    profile.country = data.get("country", profile.country)
    profile.references = data.get("references", profile.references)

    db.session.commit()

    return jsonify(profile.serialize()),200

    
