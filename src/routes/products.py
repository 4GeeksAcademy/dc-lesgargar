#Products routes 

from flask import Blueprint, jsonify, request
from models import ProductImage, db, Product, Category
from utilss.auth import admin_required

products_bp = Blueprint("products", __name__)

#get all products
@products_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify([
        {
            **product.serialize(),
            "images": [img.serialize() for img in product.images],
            "categories": [categ.name for categ in product.categories]
        }
        for product in products
    ]), 200

#get one product
@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        **product.serialize(),
        "images": [img.serialize() for img in product.images],
        "categories": [categ.name for categ in product.categories]
    }), 200

#--Post products for ADMIN user only--
@products_bp.route("/products", methods=["POST"])
@admin_required
def new_product(user):
    data = request.json

    product = Product(
        name = data["name"],
        description = data["description"],
        price = data["price"]
    )

    db.session.add(product)
    db.session.flush()

    images = data.get("images", None)

    if images:
        for url in images:
            product.images.append(ProductImage(url=url))

    db.session.commit()

    return jsonify({**product.serialize(), "images":images or []}), 201

#--Edit a product only ADMIN--
@products_bp.route("/products/<int:product_id>", methods = ["PUT"])
@admin_required
def edit_product(user, product_id):
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
def delete_product(user, product_id):
    product  = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg":"Product deleted"})

#upload prod images only ADMIN (url)
@products_bp.route("/products/<int:product_id>/images", methods = ["POST"])
@admin_required
def add_product_img(user, product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json

    image = ProductImage(
        url = data["url"],
        product = product
    )
    db.session.add(image)
    db.session.commit()
    
    return jsonify({
    "msg": "Image added",
    "image": image.serialize()
    }), 201


#get all images from 1 product
@products_bp.route("/products/<int:product_id>/images", methods=["GET"])
def get_product_images(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify([image.serialize() for image in product.images]), 200

#get 1 image
@products_bp.route("/products/images/<int:image_id>", methods=["GET"])
def get_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    return jsonify(image.serialize()), 200

#delete 1 image
@products_bp.route("/products/images/<int:image_id>", methods = ["DELETE"])
@admin_required
def delete_image(user, image_id):
    image = ProductImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()

    return jsonify({"msg":"image deleted",}),200
