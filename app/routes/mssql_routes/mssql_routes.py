from flask import Blueprint
from app.controllers.mssql_controllers.mssql_mutasi_controller import MSSQLTransaksiController

mssql_bp = Blueprint("mssql", __name__)

mssql_bp.route("/data-all-reseller-bulanan",methods=["GET"])(MSSQLTransaksiController.get_all_realtime_by_bulan)

mssql_bp.route("/data-by-reseller-bulanan/<kode_transaksi>",methods=["GET"])(MSSQLTransaksiController.get_by_id_realtime_by_bulan)
