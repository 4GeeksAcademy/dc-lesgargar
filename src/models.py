from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, Integer, DateTime, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from enum import Enum

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

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
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default= True, server_default="true")
    is_verified: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False,  server_default="false")
    role: Mapped[str] = mapped_column(String(120), default="customer")

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
    profile: Mapped["Profile"] = relationship(back_populates = "user", cascade="all, delete-orphan", uselist=False)


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

class Profile(db.Model):
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(120))
    street: Mapped[str] = mapped_column(String(120))
    neighborhood: Mapped[str] = mapped_column(String(120))
    postal_code : Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(120))
    country:Mapped[str] = mapped_column(String(120))
    references: Mapped[str] = mapped_column(String(120))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    def serialize(self):
        return{
            "id":self.id,
            "phone":self.phone,
            "street": self.street,
            "neighborhood": self.neighborhood,
            "postalCode": self.postal_code,
            "city": self.city,
            "country": self.country,
            "references":self.references

        }

    user: Mapped["User"] = relationship(back_populates = "profile")
    

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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates = "wishlist")
    items : Mapped[List["WishlistItem"]] = relationship(back_populates= "wishlist", cascade="all, delete-orphan")

    def serialize(self):
        return{
            "id":self.id
        }

class WishlistItem(db.Model):
    __tablename__ = "wishlist_item"

    wishlist_id : Mapped[int] = mapped_column(ForeignKey("wishlists.id"), primary_key = True, nullable=False)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True, nullable=False)
    added_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    wishlist: Mapped["Wishlist"] = relationship(back_populates = "items")
    prdoduct: Mapped["Product"] = relationship()


class Cart(db.Model):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key = True)

    user_id: Mapped[int| None] = mapped_column(ForeignKey("users.id"), nullable=True)
    guest_token: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True)
    user : Mapped["User"] = relationship(back_populates = "cart")
    items : Mapped[List["CartItem"]] = relationship(back_populates = "cart", cascade="all, delete-orphan")
    cascade="all, delete-orphan"

    def serialize(self):
        return{
            "id":self.id
        }

#Cart item model (association object)
class CartItem(db.Model):
    __tablename__ = "cart_item"

    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id"), primary_key=True, nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), primary_key=True, nullable=False
    )

    quantity: Mapped[int] = mapped_column(Integer, default=1)
    added_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    snapshot_price: Mapped[int] = mapped_column(Integer, nullable=True)


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

    product_id: Mapped[int] = mapped_column( ForeignKey("products.id"), nullable=False )

    product: Mapped["Product"] = relationship(back_populates="images")


class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    guest_email: Mapped[str | None] = mapped_column(String(120))

    total: Mapped[int] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String(30), default="pending")

    created_at: Mapped[datetime] = mapped_column( DateTime, default= datetime.now)

    items: Mapped[List["OrderItem"]] = relationship(back_populates= "order", cascade = "all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    quantity: Mapped[int] = mapped_column(Integer)

    snapshot_price:Mapped[int] = mapped_column(Integer)

    order: Mapped["Order"] = relationship(back_populates="items")


