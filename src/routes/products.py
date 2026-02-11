#Products routes 

from flask import Blueprint, jsonify, request
from models import ProductImage, db, Product, Category
from utilss.auth import admin_required

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify([
        {
            **product.serialize(),
            "images":[img.url for img in product.images],
            "categories":[categ.name for categ in product.categories] 
        }
        for product in products
    ])



@products_bp.route("/products/<int:product_id>", methods=["GET"])
@admin_required
def get_product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        **product.serialize(),
        "images": [img.url for img in product.images],
        "categories": [categ.name for categ in product.categories]
    })



#--Post products for ADMIN user only--
@products_bp.route("/products", methods=["POST"])
def new_product():
    data = request.json

    product = Product(
        name = data["name"],
        description = data["description"],
        price = data["price"]
    )
    db.session.add(product)
    db.session.commit()

    return jsonify(product.serialize()), 201


#--Edit a product only ADMIN--
@products_bp.route("/products/<int:product_id>", methods = ["PUT"])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)

    db.session.commit()

    return jsonify(product.serialize())

#--Delete a product only ADMIN --
@products_bp.route("/products/<int:product_id>", methods=["DELETE"])
@admin_required
def delete_product(product_id):
    product  = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg":"Product deleted"})

#upload prod images only ADMIN (url)
@products_bp.route("/products/<int:product_id>/images", methods = ["POST"])
@admin_required
def add_product_img(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json

    image = ProductImage(
        url = data["url"],
        product = product
    )
    db.session.add(image)
    db.session.commit()

    return jsonify({"msg":"Image added"})