#in this file we get the wishlist or if theres no wl this f creates a new one.
#to be used in wishlist routes
from flask import request
from models import Wishlist,db


def get_or_create_wishlist(user_id):
    wishlist = Wishlist.query.filter_by(user_id=user_id).first()
    if not wishlist:
        wishlist = Wishlist(user_id=user_id)
        db.session.add(wishlist)
        db.session.commit()
    return wishlist
    