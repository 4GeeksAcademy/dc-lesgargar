from flask import request, jsonify, Blueprint
from utilss.wishlist import get_or_create_wishlist
from utilss.auth import login_required
from models import db, WishlistItem


#create blueprint
wishlist_bp = Blueprint("wishlist", __name__,  url_prefix="/wishlist")



@wishlist_bp.route("/", methods=["GET"])
@login_required
def get_wishlist(user):
    wishlist = get_or_create_wishlist(user.id)

    return jsonify({
        "wishlist_id" : wishlist.id,
        "items" : [
          {
            "product_id": item.product_id,
            "name": item.product.name,
            "price": item.product.price,
          }
          for item in wishlist.items
        ]
    }), 200


#add items to the wishlist
@wishlist_bp.route("/items", methods=["POST"])
@login_required
def add_item(user):
    data = request.json
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error":"product_id required"}), 400
    
    wishlist = get_or_create_wishlist(user.id)
    
    item = WishlistItem.query.filter_by(
        wishlist_id= wishlist.id,
        product_id = product_id
        ).first()
    
    if item:
        return jsonify({"msg":"Item already exists in wishlist"}),400
    
    item = WishlistItem(
        wishlist_id = wishlist.id,
        product_id = product_id
    )
    db.session.add(item)
    db.session.commit()
    response = {"msg":"Item added to the wishlist"}

    return jsonify(response), 200



#delete items from wishlist
@wishlist_bp.route("/items/<int:product_id>", methods=["DELETE"])
@login_required
def delete_item( user, product_id):
    wishlist = get_or_create_wishlist(user.id)
    item = WishlistItem.query.filter_by(
        wishlist_id = wishlist.id,
        product_id =  product_id
    ).first()

    if not item:
        return jsonify({"msg":"Nothing to do, item not found"}), 404
    
    db.session.delete(item)
    db.session.commit()

    return jsonify({"msg":"item removed"}),200

#delete wishlist
@wishlist_bp.route("/", methods = ["DELETE"])
@login_required
def clear_wishlist(user):
    wishlist = get_or_create_wishlist(user.id)
    WishlistItem.query.filter_by(wishlist_id = wishlist.id).delete()
    db.session.commit()
    return jsonify({"msg":"Wishlist deleted"}),200