from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from . import db


class UserModel(db.Model):

    __tablename__ = "users"
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    name = db.Column(
        db.String, 
        nullable=False
    )
    email = db.Column(
        db.String, 
        nullable=False, 
        unique=True
    )
    password = db.Column(
        db.String, 
        nullable=False
    )
    pis = db.Column(
        db.String,
        index=False,
        unique=True,
        nullable=False
    )
    cpf = db.Column(
        db.String,
        index=False,
        unique=True,
        nullable=False
    )
    address = db.Column(
        db.String,
        index=False,
        unique=False,
        nullable=False
    )
    city = db.Column(
        db.String,
        index=True,
        unique=False,
        nullable=False
    )
    complement = db.Column(
        db.String,
        index=False,
        unique=False,
        nullable=True
    )
    country = db.Column(
        db.String,
        index=False,
        unique=False,
        nullable=False
    )
    number = db.Column(
        db.String,
        index=False,
        unique=True,
        nullable=True
    )
    postal_code = db.Column(
        db.String,
        index=False,
        unique=False,
        nullable=False
    )
    state = db.Column(
        db.String,
        index=False,
        unique=False,
        nullable=False
    )
