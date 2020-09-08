from flask import Blueprint
from flask_restful import Api

from . import infomation

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp, catch_all_404s=True)

user_api.add_resource(infomation.UserResource, '/v1/users/<int:user_id>')
