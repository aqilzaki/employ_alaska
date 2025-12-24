from flask_jwt_extended import jwt_required
from app.middlewares.active_account_required import active_account_required
from app.middlewares.role_required import role_required

class KaryawanController:

    @staticmethod
    @jwt_required()
    @active_account_required
    @role_required(
        jabatan=["HRD", "Manager"],
        departemen=["Human Resource"]
    )
    def get_all():
        return {
            "success": True,
            "message": "Akses diterima"
        }, 200
