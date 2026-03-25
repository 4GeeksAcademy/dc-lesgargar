from flask import Blueprint, jsonify, request
from models import db, Category, Product
from utilss.auth import admin_required

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

#create category
@categories_bp.route("/", methods = ["POST"])
@admin_required
def create_category(user):
    data = request.json
    if not data or not data.get("name"):
        return jsonify({"msg":"Category name is required"})
    
    existing_category = Category.query.filter_by(name = data["name"]).first()
    if existing_category:
        return jsonify({"msg":"Category already exists"}),409
    
    category = Category(name = data["name"])
    db.session.add(category)
    db.session.commit()

    return jsonify(category.serialize()),201

@categories_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.serialize() for category in categories])

#get one category
@categories_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)

    return jsonify({
        "id": category.id,
        "name": category.name,
        "products": [
            {
                **product.serialize(),
                "categories": [c.serialize() for c in product.categories],
                "images": [img.serialize() for img in product.images]
            }
            for product in category.products
        ]
    }),200

#edit
@categories_bp.route("/<int:category_id>", methods=["PUT"])
@admin_required
def edit_category(user, category_id):
    category = Category.query.get_or_404(category_id)
    data = request.json
    if "name" in data:
        existing_category = Category.query.filter(
            Category.name == data["name"],
            Category.id != category_id
        ).first()

        if not data or not data.get("name"):
            return jsonify({"msg":"Category name is required"})

        if existing_category:
            return jsonify({"msg":"This category already exists"}), 409
        
        category.name = data["name"]
    
    db.session.commit()
    return jsonify(category.serialize()), 200 

#delete category
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@admin_required
def delete_categry(user, category_id):
    category = Category.query.get_or_404(category_id)

    db.session.delete(category)
    db.session.commit()

    return jsonify({"msg":"Cateegory deleted"}), 200


