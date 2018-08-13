from flask import flash, redirect, render_template, request , session, abort, url_for, Markup
from ung_dung import app
from ung_dung.Xu_ly.Nhan_vien_Ban_hang.Xu_ly_3L import *

def thongtin():
    Nhan_vien_dang_nhap = session["Nhan_vien_ban_hang_dang_nhap"]
    Chuoi_HTML_nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_dang_nhap)
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_tivi_theo_nhan_vien = Doc_Danh_sach_Tivi_theo_Nhan_vien(Danh_sach_Tivi, Nhan_vien_dang_nhap)
    return Chuoi_HTML_nhan_vien, Danh_sach_tivi_theo_nhan_vien

@app.route("/Nhan-vien-Ban-hang/Xem-Danh-sach-Tivi",methods=['GET','POST'])
def Xemdanhsachtivi():
    Chuoi_HTML_nhan_vien, Danh_sach_tivi_theo_nhan_vien = thongtin()

    Danh_sach_tivi_xem = Danh_sach_tivi_theo_nhan_vien

    Chuoi_HTML_danh_sach_tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_tivi_xem)
    return render_template("Nhan_vien_Ban_hang/MH_Xem_Danh_sach_Tivi.html",Chuoi_HTML_Nhan_vien=
    Chuoi_HTML_nhan_vien, Chuoi_HTML_Danh_sach_Tivi= Chuoi_HTML_danh_sach_tivi)

@app.route("/nhan-vien-ban-hang/dang-nhap",methods=['GET','POST'])
def NhanVienBanHangDangNhap():
    if (session.get("Nhan_vien_ban_hang_dang_nhap")):
        return redirect(url_for('NhanVienBanHangDanhSachTivi'))
    Cong_ty=Doc_Cong_ty()
    Ten_dang_nhap=''
    Mat_khau=''
    Chuoi_thong_bao='Xin vui lòng nhập tên đăng nhập và mật khẩu'
    if (request.form.get('Th_Ten_dang_nhap')):
        Ten_dang_nhap=request.form.get('Th_Ten_dang_nhap')
        Mat_khau=request.form.get('Th_Mat_khau')
        Nhan_vien=Dang_nhap_Nhan_vien(Cong_ty['Danh_sach_Nhan_vien_Ban_hang'],Ten_dang_nhap,Mat_khau)
        if (Nhan_vien!=None):
            session["Nhan_vien_ban_hang_dang_nhap"]=Nhan_vien
            return redirect(url_for('NhanVienBanHangDanhSachTivi'))
        else:
            Chuoi_thong_bao='Đăng nhập không thành công'
    return render_template("Nhan_vien_Ban_hang/MH_Dang_nhap.html",Chuoi_Thong_bao=Chuoi_thong_bao)

@app.route("/nhan-vien-ban-hang/danh-sach-tivi",methods=['GET','POST'])
def NhanVienBanHangDanhSachTivi():
    Nhan_vien_Dang_nhap = session['Nhan_vien_ban_hang_dang_nhap']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    Dia_chi_MH='/Nhan-vien-Ban-hang/Xem-Danh-sach-Tivi'
    Chuoi_Tra_cuu=''
    if (request.method == 'POST'):
        Ma_so = request.form.get('Th_Ma_so')
        if (Ma_so == 'DANH_SACH'):
            Dia_chi_MH='/Nhan-vien-Ban-hang/Xem-Danh-sach-Tivi'
        if (Ma_so == 'TRA_CUU' and request.form.get('Th_Chuoi_Tra_cuu')!=''):
                Chuoi_Tra_cuu = request.form.get('Th_Chuoi_Tra_cuu')
                Dia_chi_MH='/Nhan_vien_Ban_hang/Tra_cuu/' + Chuoi_Tra_cuu
        if (Ma_so == 'DOANH_THU'):
            Dia_chi_MH = '/nhan-vien-ban-hang/thong-ke'
   
    return render_template("Nhan_vien_Ban_hang/MH_Chinh.html", Dia_chi_MH=Dia_chi_MH, 
    Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien, Chuoi_Tra_cuu=Chuoi_Tra_cuu)

@app.route("/Nhan_vien_Ban_hang/Ban/<string:Ma_so>/",methods=['GET','POST'])
def NhanVienBanHangBanHang(Ma_so):
    Nhan_vien_Dang_nhap = session['Nhan_vien_ban_hang_dang_nhap']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    Danh_sach_Tivi_theo_Nhan_vien = Doc_Danh_sach_Tivi_theo_Nhan_vien(Danh_sach_Tivi, Nhan_vien_Dang_nhap)
    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi_theo_Nhan_vien, Ma_so)

    if (Tivi_Chon != None):
        So_luong = 1
        Thong_bao=''
        if (request.method == 'POST'):
            So_luong = int(request.form.get('Th_So_luong'))
            Tien = Ban_Tivi(Nhan_vien_Dang_nhap,Tivi_Chon, So_luong)
            Thong_bao = "Vừa bán " + str(So_luong) + " Tivi " + Tivi_Chon['Ten'] + \
            " - Tiền phải trả là: {:,}".format(Tien).replace(",",".")
            Ghi_Tivi(Tivi_Chon)
        Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, So_luong)
        return render_template("Nhan_vien_Ban_hang/MH_Ban_Tivi.html", Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)

@app.route("/Nhan_vien_Ban_hang/Tra_cuu/<string:Chuoi_Tra_cuu>/",methods=['GET','POST'])
def NhanVienBanHangTraCuu(Chuoi_Tra_cuu):
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi_theo_Nhan_vien = thongtin()

    Danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi_theo_Nhan_vien)

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)
    return render_template("Nhan_vien_Ban_hang/MH_Xem_Danh_sach_Tivi.html",\
    Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien, \
    Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi,\
    Chuoi_Tra_cuu=Chuoi_Tra_cuu)

@app.route("/nhan-vien-ban-hang/thong-ke",methods=['GET','POST'])
def NhanVienBanHangThongKe():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi_theo_Nhan_vien = thongtin()
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi_theo_Nhan_vien, Ngay)
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_ban,Ngay)
    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)
    return render_template("Nhan_vien_Ban_hang/MH_Xem_Doanh_thu.html", Chuoi_HTML_Thong_ke_Tivi=
    Chuoi_HTML_Thong_ke_Tivi)

@app.route("/Nhan_vien_Ban_hang/Dang_xuat/",methods=['GET','POST'])
def NhanVienBanHangDangXuat():
    session.pop('Nhan_vien_ban_hang_dang_nhap',None)
    return redirect(url_for('NhanVienBanHangDangNhap'))