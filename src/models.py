from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(
        String(120), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    role: Mapped[str] = mapped_column(String(120), default="customer", nullable= False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name":self.name,
            "role": self.role
            # do not serialize the password, its a security breach
        }
    
    wishlist: Mapped[List["Wishlist"]] = relationship(back_populates = "user", cascade="all, delete-orphan")
    cart : Mapped[List["Cart"]] = relationship(back_populates = "user", cascade="all, delete-orphan")


product_category = db.Table(
    "product_category",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id"), primary_key=True)
)


wishlist_product = db.Table(
    "wishlist_product",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
    db.Column("wishlist_id", db.Integer, db.ForeignKey("wishlists.id"), primary_key=True)
    
)

class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


    categories = db.relationship(
        "Category",
        secondary = product_category,
        back_populates= "products"
    )

    images: Mapped[List["ProductImage"]] = relationship(back_populates="product", cascade= "all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price

        }

class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(120), unique = True, nullable = False)

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name
        }

    products = db.relationship(
        "Product",
        secondary = product_category,
        back_populates = "categories"
    )

#Favorites list model
class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id: Mapped[int] = mapped_column(primary_key = True)
    #users.id es porque asi se llama el __tablename__
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates = "wishlist")

    def serialize(self):
        return{
            "id":self.id
        }


class Cart(db.Model):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key = True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user : Mapped["User"] = relationship(back_populates = "cart")
    items : Mapped[List["CartItem"]] = relationship(back_populates = "cart")

    def serialize(self):
        return{
            "id":self.id
        }

#Cart item model (association object)
class CartItem(db.Model):
    __tablename__ = "cart_item"

    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id"), primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), primary_key=True
    )

    quantity: Mapped[int] = mapped_column(Integer, default=1)
    added_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    cart: Mapped["Cart"] = relationship(back_populates = "items")
    product: Mapped["Product"] = relationship()

    def serialize(self):
        return{
            "quantity":self.quantity
        }
    
class ProductImage(db.Model):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key= True)
    url:Mapped[str] = mapped_column(String(255), nullable= False)

    product_id = Mapped[int] = mapped_column( ForeignKey("products.id"), nullable=False )

    product: Mapped["Product"] = relationship(back_populates="images")

