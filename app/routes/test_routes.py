from flask import Blueprint
from flask_jwt_extended import create_access_token

test_bp = Blueprint("test", __name__)

@test_bp.route("/test-jwt",methods=["GET"])
def test_jwt():
    token = create_access_token(identity="TEST-ID")
    return {"token": token}
