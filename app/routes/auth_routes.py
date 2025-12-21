from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/login", methods=["POST"])(AuthController.login)
auth_bp.route("/refresh", methods=["POST"])(AuthController.refresh)
auth_bp.route("/logout", methods=["POST"])(AuthController.logout)