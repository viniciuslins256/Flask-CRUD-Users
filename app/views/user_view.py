from app.helpers.user_validate import UserValidate
from app.models.user_model import UserModel
from datetime import timedelta
from flask import Blueprint, current_app, request 
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from http import HTTPStatus
from sqlalchemy import or_


bp_login = Blueprint("login_view", __name__, url_prefix="/login")
bp_register = Blueprint("register_view", __name__, url_prefix="/register")
bp_user = Blueprint("user_view", __name__, url_prefix="/users")


@bp_login.route("/", methods=["POST"], strict_slashes=False)
def login():
    res = request.get_json()
    identifier = ""
    if "email" in res:
        identifier = "email"
        email = res.get("email") 
        found_user: UserModel = UserModel.query.filter_by(email=email).first()
    elif "cpf" in res:
        identifier = "cpf"
        cpf = res.get("cpf") 
        found_user: UserModel = UserModel.query.filter_by(cpf=cpf).first()
    elif "pis" in res:
        identifier = "pis"
        pis = res.get("pis") 
        found_user: UserModel = UserModel.query.filter_by(pis=pis).first()
    
    password = res.get("password")

    found_user: UserModel = UserModel.query.filter_by(email=email).first()

    if not found_user or not found_user.password == password:
        return {"error": f"Incorrect {identifier} or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(
        identity=found_user.id, expires_delta=timedelta(days=7)
    )
    return {"accessToken": access_token}, HTTPStatus.OK


@bp_register.route("/", methods=["POST"], strict_slashes=False)
def register():
    session = current_app.db.session

    res = request.get_json()

    try:
        UserValidate(res)
    except ValueError as err:
        return {"error": err.message}, HTTPStatus.BAD_REQUEST

    name = res.get("name")
    email = res.get("email")
    cpf = res.get("cpf")
    pis = res.get("pis")
    password = res.get("password")
    address = res.get("address")
    city = res.get("city")
    complement = res.get("complement")
    country = res.get("country")
    number = res.get("number")
    postal_code = res.get("postal_code")
    state = res.get("state")



    verify_email: UserModel = UserModel.query.filter_by(email=email).first()
    if verify_email:
        return {"error": f"User with email '{email}' already exists"}, HTTPStatus.FORBIDDEN

    verify_pis: UserModel = UserModel.query.filter_by(pis=pis).first()
    if verify_pis:
        return {"error": f"User with pis '{pis}' already exists"}, HTTPStatus.FORBIDDEN

    verify_cpf: UserModel = UserModel.query.filter_by(cpf=cpf).first()
    if verify_cpf:
        return {"error": f"User with CPF '{cpf}' already exists"}, HTTPStatus.FORBIDDEN

    new_user = UserModel(
        name=name,
        email=email,
        cpf = cpf,
        pis = pis,
        password = password,
        address = address,
        city = city,
        complement = complement,
        country = country,
        number = number,
        postal_code = postal_code,
        state = state,
    )
    new_user.password = password
    session.add(new_user)

    session.commit()

    access_token = create_access_token(
        identity=new_user.id, expires_delta=timedelta(days=7)
    )

    return {
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "cpf": new_user.cpf,
            "pis": new_user.pis,
            "address": new_user.address,
            "city": new_user.city,
            "complement": new_user.complement,
            "country": new_user.country,
            "number": new_user.number,
            "postal_code": new_user.postal_code,
            "state": new_user.state
        }
    }, HTTPStatus.CREATED


@bp_user.route("/self", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_yourself():

    user_id = get_jwt_identity()
    user: UserModel = UserModel.query.filter_by(id=user_id).first()

    if not user:
        return {"error": "You are not logged in!"}, HTTPStatus.NOT_FOUND

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "cpf": user.cpf,
            "pis": user.pis,
            "address": user.address,
            "city": user.city,
            "complement": user.complement,
            "country": user.country,
            "number": user.number,
            "postal_code": user.postal_code,
            "state": user.state
        }
    }, HTTPStatus.OK


@bp_user.route("/self", methods=["DELETE"])
@jwt_required()
def delete_user():
    session = current_app.db.session

    user_id = get_jwt_identity()
    user: UserModel = UserModel.query.filter_by(id=user_id).first()

    if not user:
        return {"error": f"You are not logged in!"}, HTTPStatus.NOT_FOUND

    session.delete(user)
    session.commit()

    return {"message": f"The user {user.email} was deleted"}, HTTPStatus.OK


@bp_user.route("/", methods=["PATCH"], strict_slashes=False)
@jwt_required()
def update_user():

    user_id = get_jwt_identity()
    user: UserModel = UserModel.query.filter_by(id=user_id).first()

    if not user:
        return {"error": "User not registered"}, HTTPStatus.NOT_FOUND

    data = request.get_json()

    if "email" in data:
        found_email = UserModel.query.filter_by(email=data.get("email")).first()
        if found_email:
            return {
                "error": "This email address is already and being used"
            }, HTTPStatus.CONFLICT
    
    if "pis" in data:
        return {
            "error": "Not is possible update to PIS"
        }, HTTPStatus.CONFLICT

    if "cpf" in data:
        return {
            "error": "Not is possible update to CPF"
        }, HTTPStatus.CONFLICT

    [setattr(user, key, value) for key, value in data.items()]

    session = current_app.db.session
    session.add(user)
    session.commit()

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "cpf": user.cpf,
            "pis": user.pis,
            "address": user.address,
            "city": user.city,
            "complement": user.complement,
            "country": user.country,
            "number": user.number,
            "postal_code": user.postal_code,
            "state": user.state
        }
    }, HTTPStatus.OK


@bp_user.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def users_list():
    list_of_users = UserModel.query.all()

    return {
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "cpf": user.cpf,
                "pis": user.pis,
                "address": user.address,
                "city": user.city,
                "complement": user.complement,
                "country": user.country,
                "number": user.number,
                "postal_code": user.postal_code,
                "state": user.state
            }
            for user in list_of_users
        ]
    }, HTTPStatus.OK


@bp_user.route("/<int:user_id>/about", methods=["GET"])
@jwt_required()
def user_info(user_id):

    user: UserModel = UserModel.query.filter_by(id=user_id).first()

    if not user:
        return {
            "error": "The ID not is valid!"
        }, HTTPStatus.NOT_FOUND

    user_info = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "cpf": user.cpf,
        "pis": user.pis,
        "address": user.address,
        "city": user.city,
        "complement": user.complement,
        "country": user.country,
        "number": user.number,
        "postal_code": user.postal_code,
        "state": user.state
    }

    return {
        "user": user_info,
    }, HTTPStatus.OK
