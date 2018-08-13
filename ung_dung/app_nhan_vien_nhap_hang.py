from flask import flash, redirect, render_template, request , session, abort, url_for, Markup
from ung_dung import app
from ung_dung.Xu_ly.Nhan_vien_Nhap_hang.Xu_ly_3L import *

def thongtinnhap():
    Nhan_vien_dang_nhap = session['Nhan_vien_nhap_hang_dang_nhap']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_dang_nhap)
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    return Chuoi_HTML_Nhan_vien, Danh_sach_Tivi

@app.route("/Nhan-vien-Nhap-hang/Xem-Danh-sach-Tivi",methods=['GET','POST'])
def Xemdanhsachtivinhap():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = thongtinnhap()
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi)
    return render_template("Nhan_vien_Nhap_hang/MH_Xem_Danh_sach_Tivi.html",Chuoi_HTML_Danh_sach_Tivi=\
    Chuoi_HTML_Danh_sach_Tivi)

@app.route("/nhan-vien-nhap-hang/dang-nhap",methods=['GET','POST'])
def NhanVienNhapHangDangNhap():
    if (session.get('Nhan_vien_nhap_hang_dang_nhap')):
        return redirect(url_for('NhanVienNhapHangDanhSachTivi'))
    Cong_ty = Doc_Cong_ty()
    Ten_dang_nhap = ''
    Mat_khau = ''
    Chuoi_thong_bao = 'Xin vui lòng nhập tên đăng nhập và mật khẩu'
    if (request.form.get('Th_Ten_dang_nhap')):
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Nhan_vien_Nhap_hang"],Ten_dang_nhap, Mat_khau)
        if (Nhan_vien != None):
            session['Nhan_vien_nhap_hang_dang_nhap'] = Nhan_vien
            return redirect(url_for('NhanVienNhapHangDanhSachTivi'))
        else:
            Chuoi_thong_bao = 'Đăng nhập không thành công'
    return render_template("Nhan_vien_Nhap_hang/MH_Dang_nhap.html",Chuoi_Thong_bao=Chuoi_thong_bao)

@app.route("/nhan-vien-nhap-hang/danh-sach-tivi",methods=['GET','POST'])
def NhanVienNhapHangDanhSachTivi():
    Nhan_vien_Nhap_hang_Dang_nhap = session['Nhan_vien_nhap_hang_dang_nhap']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Nhap_hang_Dang_nhap)

    Dia_chi_MH = "/Nhan-vien-Nhap-hang/Xem-Danh-sach-Tivi"
    Chuoi_Tra_cuu = ''
    if (request.method == 'POST'):
        Ma_so = request.form.get('Th_Ma_so')
        if (Ma_so == 'DANH_SACH'):
            Dia_chi_MH='/Nhan-vien-Nhap-hang/Xem-Danh-sach-Tivi'
        if (Ma_so == 'TRA_CUU' and request.form.get('Th_Chuoi_Tra_cuu')!=''):
            Chuoi_Tra_cuu = request.form.get('Th_Chuoi_Tra_cuu')
            Dia_chi_MH='/Nhan_vien_Nhap_hang/Tra_cuu/' + Chuoi_Tra_cuu
        if (Ma_so == 'PHIEU_NHAP'):
            Dia_chi_MH = '/nhan-vien-nhap-hang/thong-ke'
    return render_template("Nhan_vien_Nhap_hang/MH_Chinh.html",Dia_chi_MH=Dia_chi_MH, Chuoi_HTML_Nhan_vien=\
    Chuoi_HTML_Nhan_vien)

@app.route("/Nhan_vien_Nhap_hang/Tra_cuu/<string:Chuoi_Tra_cuu>/",methods=['GET','POST'])
def NhanVienNhapHangTraCuu(Chuoi_Tra_cuu):
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = thongtinnhap()

    Danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi)

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)
    return render_template("Nhan_vien_Nhap_hang/MH_Xem_Danh_sach_Tivi.html",\
    Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien, \
    Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi,\
    Chuoi_Tra_cuu=Chuoi_Tra_cuu)

@app.route("/Nhan_vien_Nhap_hang/Nhap/<string:Ma_so>/",methods=['GET','POST'])
def NhanVienNhapHangNhapHang(Ma_so):
    Nhan_vien_Dang_nhap = session['Nhan_vien_nhap_hang_dang_nhap']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)

    if (Tivi_Chon != None):
        So_luong = 1
        Thong_bao=''
        if (request.method == 'POST'):
            So_luong = int(request.form.get('Th_So_luong'))
            Tien = Nhap_Tivi(Nhan_vien_Dang_nhap,Tivi_Chon, So_luong)
            Thong_bao = "Vừa nhập " + str(So_luong) + " Tivi " + Tivi_Chon['Ten'] + \
            " - Tiền phải trả là: {:,}".format(Tien).replace(",",".")
            Ghi_Tivi(Tivi_Chon)
        Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, So_luong)
        return render_template("Nhan_vien_Nhap_hang/MH_Nhap_Tivi.html", Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)

@app.route("/nhan-vien-nhap-hang/thong-ke",methods=['GET','POST'])
def NhanVienNhapHangThongKe():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = thongtinnhap()
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_nhap = Danh_sach_Tivi_Nhap_Theo_ngay(Danh_sach_Tivi, Ngay)
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_nhap,Ngay)
    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)
    return render_template("Nhan_vien_Nhap_hang/MH_Xem_Phieu_nhap.html", Chuoi_HTML_Thong_ke_Tivi=
    Chuoi_HTML_Thong_ke_Tivi)

@app.route("/Nhan_vien_Nhap_hang/Dang_xuat/",methods=['GET','POST'])
def NhanVienNhapHangDangXuat():
    session.pop('Nhan_vien_nhap_hang_dang_nhap',None)
    return redirect(url_for('NhanVienNhapHangDangNhap'))