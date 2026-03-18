from flask import Blueprint, jsonify, request
from models import db, OrderItem, Order, Product, CartItem
from utilss.auth import login_optional, login_required, admin_required
from utilss.cart import get_or_create_cart

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

#checkout
@orders_bp.route("/checkout", methods=["POST"])
@login_optional
def checkout(user):
    data = request.json or{}

    #step1 get cart
    cart, guest_token = get_or_create_cart(user)

    if not cart. items:
        return jsonify({"msg":"Cart is empty"}), 400
    
    #creeate order 
    order = Order()

    if user:
        order.user_id = user.id
    else:
        guest_email = data.get("guest_email")

        if not guest_email:
            return jsonify({"msg":"guest email required"})
        
        order.guest_email = guest_email

    total = 0

    #copy cart items 
    for item in cart.items:

        order_item = OrderItem(
            product_id = item.product_id,
            quantity = item.quantity,
            snapshot_price = item.product.price
        )

        total += item.product.price * item.quantity

        order.items.append(order_item)
    
    order.total = total

    db.session.add(order)

    #empty cart
    CartItem.query.filter_by(cart_id = cart.id).delete()
    db.session.commit()

    return jsonify({
        "msg":"Order created", 
        "order_id":order.id,
        "total":total        
    }), 201


#get user orders 
@orders_bp.route("/", methods=["GET"])
@login_required
def get_orders(user):

    orders = Order.query.filter_by(user_id=user.id).all()

    return jsonify([o.serialize() for o in orders]), 200


#get 1 order in specific
@orders_bp.route("/<int:order_id>", methods=["GET"])
@login_required
def get_order(user, order_id):

    order = Order.query.get(order_id)

    if not order or order.user_id != user.id:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order.serialize()), 200


#update order status only for admin 

@orders_bp.route("/<int:order_id>", methods=["PATCH"])
@admin_required
def update_order(admin, order_id):

    order = Order.query.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.json

    if "status" in data:
        order.status = data["status"]

    db.session.commit()

    return jsonify(order.serialize()), 200

