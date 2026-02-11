#Cart routes
from flask import Blueprint, jsonify, request
from utilss.cart import get_or_create_cart
from models import CartItem, db



#Create blueprint to be imported to init and finally to app.py
cart_bp = Blueprint("cart", __name__, url_prefix="/api/carts")

@cart_bp.route("/", methods=["GET"])

def get_cart():

    #get_or_create validates user, guest and if cart exists, if not, it will be created
    cart, guest_token = get_or_create_cart()

    return jsonify({
        "cart_id":cart.id,
        "items":[
            {
            "product.id":item.product_id,
            "name":item.product.name,
            "price":item.product.price,
            "quantity": item.quantity,
            "subtotal":item.product.price * item.quantity
            }
            for item in cart.items
        ],
        "total": sum(
            item.product.price * item.quantity
            for item in cart.items
        )
    }),200


#add products to the cart
@cart_bp.route("/items", methods=["POST"])
def add_item():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"error":"product_id required"}), 400
    
    cart, guest_token = get_or_create_cart()

    item = CartItem.query.filter_by(
        cart_id = cart.id,
        product_id = product_id,
    ).first()

    #if item exists just sum to the qty, if not is created as new item in the cart
    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(item)

    db.session.commit()

    response = {"msg":"Item succesfully added"}

    if guest_token:
        response["guest_token"] = guest_token
    
    return jsonify(response), 200


#edit cart
@cart_bp.route("/items/<int:product_id>", methods = ["PUT"])

def update_item(product_id):
    data = request.json
    quantity = data.get("quantity")

    if quantity is None or quantity < 1:
        return jsonify({"error":"empty qty"}), 400
    
    cart, _ = get_or_create_cart()

    item = CartItem.query.filter_by(
        cart_id = cart.id,
        product_id = product_id
    ).first()

    if not item:
        return jsonify({"error":"Item not found"}),404
    
    item.quantity =quantity
    db.session.commit()

    return jsonify({"msg":"Item updated"}),200


#delete items from cart 
@cart_bp.route("/items/<int:product_id>", methods=["DELETE"])
def remove_item(product_id):
    cart, _ = get_or_create_cart()

    item = CartItem.query.filter_by(
        cart_id = cart.id,
        product_id=product_id
    ).first()

    if not item:
        return jsonify({"error":"item not found"}),404
    
    db.session.delete(item)
    db.session.commit()

    return jsonify({"msg":"item removed from cart"}), 200

#Empty cart
@cart_bp.route("/", methods=["DELETE"])

def clear_cart():
    cart, _ = get_or_create_cart()

    CartItem.query.filter_by(cart_id = cart.id).delete()
    db.session.commit()

    return jsonify({"msg":"cart is now empty"}),200 