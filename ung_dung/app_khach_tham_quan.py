from flask import flash, redirect, render_template, request , session, abort, url_for, Markup
from ung_dung import app
from ung_dung.Xu_ly.Khach_tham_quan.Xu_ly_3L import *
@app.route("/", methods=['GET','POST'])
def index():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Chuoi_Tra_cuu=''
    if request.form.get('Th_Chuoi_Tra_cuu')!=None:
        Chuoi_Tra_cuu=request.form.get('Th_Chuoi_Tra_cuu')
        Danh_sach_Tivi=Tra_cuu_Tivi(Chuoi_Tra_cuu,Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi)
    return render_template("Khach_tham_quan/MH_Chinh.html",Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi,
    Chuoi_Tra_cuu=Chuoi_Tra_cuu)

@app.route("/khach-tham-quan", methods=['GET','POST'])
def KTQDanhSachTivi():
    Danh_sach_Tivi = Doc_danh_sach_tivi_tu_api()
    Chuoi_Tra_cuu=''
    if request.form.get('Th_Chuoi_Tra_cuu')!=None:
        Chuoi_Tra_cuu=request.form.get('Th_Chuoi_Tra_cuu')
        Danh_sach_Tivi=Tra_cuu_Tivi(Chuoi_Tra_cuu,Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi)
    return render_template("Khach_tham_quan/MH_Chinh.html",Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi,
    Chuoi_Tra_cuu=Chuoi_Tra_cuu)