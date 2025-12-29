from flask import Blueprint
from app.controllers.mssql_controllers.mssql_mutasi_controller import LaporanTestController as MSSQLTransaksiController
from app.controllers.mssql_controllers.laporan_controller import LaporanController

mssql_bp = Blueprint("mssql", __name__)

mssql_bp.route( "/laporan/transaksi/bulanan",
    methods=["GET"]
)(MSSQLTransaksiController.transaksi_bulanan)

mssql_bp.route( "/laporan/transaksi/realtime",
    methods=["GET"]
)(MSSQLTransaksiController.transaksi_realtime)


laporan_bp = Blueprint("laporan", __name__)

laporan_bp.route(
    "/profit-marketing",
    methods=["GET"]
)(LaporanController.get_laporan_transaksi)
