#in this file we get the cart validate if is user or guest also if theres no cart this f creates a new one.
#to be used in cart routes
from flask import request
from models import Cart
import uuid
from models import db

#guest id comes from frontend

def get_or_create_cart(user = None):
  #Validation if is user 
    if user:
        cart = Cart.query.filter_by(user_id= user.id).first()
        if not cart :
            cart = Cart(user_id = user.id)
            db.session.add(cart)
            db.session.commit()
        return cart, None
    
    
    #if guest
    guest_token = request.headers.get("X-guest-token")
    if not guest_token:
        guest_token = str(uuid.uuid4()) 

    cart = Cart.query.filter_by(guest_token=guest_token).first()
    if not cart:
        cart = Cart(guest_token=guest_token)
        db.session.add(cart)
        db.session.commit()

    return cart, guest_token 