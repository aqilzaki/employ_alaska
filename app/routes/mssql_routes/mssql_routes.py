from flask import Blueprint
from app.controllers.mssql_controllers.mssql_mutasi_controller import LaporanTestController as MSSQLTransaksiController
from app.controllers.mssql_controllers.mssql_mutasi_controller import LaporanPivotController
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


pivot_bp = Blueprint("pivot", __name__)

pivot_bp.route("/laporan/reseller", methods=["GET"])(LaporanPivotController.pivot_laba_reseller)
pivot_bp.route("/laporan/upline", methods=["GET"])(LaporanPivotController.pivot_laba_upline)
pivot_bp.route("/laporan/harian", methods=["GET"])(LaporanPivotController.pivot_laba_harian)
pivot_bp.route("/laporan/bulanan", methods=["GET"])(LaporanPivotController.pivot_laba_bulanan)

pivot_bp.route("/laporan/laba", methods=["GET"])(LaporanPivotController.pivot_laba)