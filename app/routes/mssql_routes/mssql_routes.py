from flask import Blueprint
from app.controllers.mssql_controllers.mssql_mutasi_controller import MSSQLMutasiController

mssql_bp = Blueprint("mssql", __name__)

mssql_bp.route(
    "/mutasi",
    methods=["GET"]
)(MSSQLMutasiController.get_by_reseller)
