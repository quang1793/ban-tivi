from flask import Flask
app=Flask(__name__, static_url_path='',static_folder='Media',template_folder='Giao_dien')
app.secret_key='239'
app.debug=True
import ung_dung.app_khach_mua_hang_online
import ung_dung.app_khach_tham_quan
import ung_dung.app_nhan_vien_ban_hang
import ung_dung.app_nhan_vien_nhap_hang
import ung_dung.app_quan_ly_ban_hang
import ung_dung.app_Quan_ly_Cong_ty
import ung_dung.app_quan_ly_nhap_hang