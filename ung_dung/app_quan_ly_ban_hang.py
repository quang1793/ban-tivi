from flask import flash, redirect, render_template, request , session, abort, url_for, Markup
from ung_dung import app
from ung_dung.Xu_ly.Quan_ly_Ban_hang.Xu_ly_3L import *
@app.route("/quan-ly-ban-hang/dang-nhap",methods=['GET','POST'])
def QuanLyBanHangDangNhap():
    if (session.get('quan_ly_ban_hang')):
        return redirect(url_for('QuanLyBanHang'))
    Cong_ty = Doc_Cong_ty()
    Ten_dang_nhap=''
    Mat_khau=''
    Chuoi_Thong_bao = 'Xin vui lòng nhập tên đăng nhập và mật khẩu'
    if (request.method == "POST"):
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty['Danh_sach_Quan_ly_Ban_hang'],Ten_dang_nhap,Mat_khau)
        if (Nhan_vien != None):
            session['quan_ly_ban_hang'] = Nhan_vien
            return redirect(url_for('QuanLyBanHang'))
        else:
            Chuoi_Thong_bao = 'Đăng nhập không hợp lệ'
    return render_template('Quan_ly_Ban_hang/MH_Dang_nhap.html', Chuoi_Thong_bao=Chuoi_Thong_bao,\
    Ten_dang_nhap=Ten_dang_nhap, Mat_khau=Mat_khau)

@app.route("/quan-ly-ban-hang",methods=['GET','POST'])
def QuanLyBanHang():
    Nhan_vien_Dang_nhap = session['quan_ly_ban_hang']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)
    Dia_chi_MH = "/Quan_ly_Ban_hang/Xem_Danh_sach_Tivi"

    if (request.method == 'POST'):
        Ma_so = request.form.get('Th_Ma_so')
        if (Ma_so == 'DANH_SACH'):
            Dia_chi_MH = '/Quan_ly_Ban_hang/Xem_Danh_sach_Tivi'
        if (Ma_so == 'TRA_CUU' and request.form.get('Th_Chuoi_Tra_cuu')!=''):
            Chuoi_Tra_cuu = request.form.get('Th_Chuoi_Tra_cuu')
            Dia_chi_MH = '/Quan_ly_Ban_hang/Tra_cuu/' + Chuoi_Tra_cuu + '/'
        if (Ma_so == 'SO_LUONG_TON'):
            Dia_chi_MH = '/Quan_ly_Ban_hang/Thong_ke/'
        if (Ma_so == 'DOANH_THU_TIVI'):
            Dia_chi_MH = '/Quan_ly_Ban_hang/Thong_ke_Doanh_thu'
        if (Ma_so == 'DOANH_THU_NHAN_VIEN'):
            Dia_chi_MH = '/Quan_ly_Ban_hang/Thong_ke_Doanh_thu_Nhan_vien'
    return render_template('/Quan_ly_Ban_hang/MH_Chinh.html',Dia_chi_MH=Dia_chi_MH,
    Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien)

def Thong_tin():
    Nhan_vien_Dang_nhap = session["quan_ly_ban_hang"]
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    return Chuoi_HTML_Nhan_vien, Danh_sach_Tivi

@app.route("/Quan_ly_Ban_hang/Xem_Danh_sach_Tivi", methods=['GET', 'POST'])
def QLBH_Xem_Danh_sach_Tivi():    
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
 # ****** Khai báo Biến ********
    Danh_sach_Tivi_Xem = Danh_sach_Tivi # Biến Kết quả
# ****** Kết xuất  ********
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(
        Danh_sach_Tivi_Xem)
    Khung = render_template('Quan_ly_Ban_hang/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien,
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)
    return Khung

@app.route("/Quan_ly_Ban_hang/Tra_cuu/<string:Chuoi_Tra_cuu>/", methods=['GET', 'POST'])
def QLBH_Tra_cuu_Tivi_theo_Chuoi_Tra_cuu(Chuoi_Tra_cuu):
    print('Cần phải vào đây: ', Chuoi_Tra_cuu)
    # ****** Khởi động Dữ liệu Nguồn/Nội bộ ********
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
 # ****** Khai báo Biến ********
    Danh_sach_Tivi_Xem = Danh_sach_Tivi
    # Biến Kết quả
    Danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi)

# ****** Kết xuất  ********
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(
        Danh_sach_Tivi_Xem)
    Khung = render_template('Quan_ly_Ban_hang/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_Tra_cuu=Chuoi_Tra_cuu, Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien,
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)
    return Khung

@app.route("/Quan_ly_Ban_hang/Thong_ke/", methods=['GET', 'POST'])
def Thong_ke_SL_ton():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    Cong_ty = Doc_Cong_ty()
    Danh_sach_Nhom_Tivi = Cong_ty["Danh_sach_Nhom_Tivi"]

    Danh_sach_Thong_ke = Thong_ke_So_luong_Ton(Danh_sach_Nhom_Tivi, Danh_sach_Tivi)
    
    Chuoi_HTML_Thong_ke_Tivi =  Tao_Chuoi_HTML_Thong_ke_SL_Ton_Tivi(Danh_sach_Thong_ke)
    return render_template(
        'Quan_ly_Ban_hang/MH_Xem_SL_Ton.html', Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route("/Quan_ly_Ban_hang/Thong_ke_Doanh_thu", methods=['GET', 'POST'])
def QLBH_Thong_ke_Doanh_thu():       
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)
    
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_ban, Ngay)
   

    Chuoi_HTML_Thong_ke_Tivi =  Tao_Chuoi_HTML_Thong_ke_Doanh_thu_Tivi(Danh_sach_Thong_ke)   
    return render_template(
            'Quan_ly_Ban_hang/MH_Xem_Doanh_thu_Tivi.html', Chuoi_HTML_Thong_ke_Tivi = Chuoi_HTML_Thong_ke_Tivi)
            
@app.route("/Quan_ly_Ban_hang/Thong_ke_Doanh_thu_Nhan_vien", methods=['GET', 'POST'])
def Thong_ke_Doanh_thu_Nhan_vien():       
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)
    
    Chuoi_HTML_Thong_ke_Nhan_vien = Tao_Chuoi_HTML_Thong_ke_Doanh_thu_Nhan_vien(Danh_sach_Tivi_ban)
    
    return render_template(
            'Quan_ly_Ban_hang/MH_Xem_Doanh_thu_Nhan_vien.html', Chuoi_HTML_Thong_ke_Nhan_vien = Chuoi_HTML_Thong_ke_Nhan_vien)


@app.route("/Quan_ly_Ban_hang/Cap_nhat/<string:Ma_so>/", methods=['GET', 'POST'])
def QuanLyBanHangCapNhat(Ma_so):
    Nhan_vien_Dang_nhap = session['quan_ly_ban_hang']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)

    if (Tivi_Chon != None):
        Don_gia_moi = 0
        Thong_bao=''
        if (request.method == 'POST'):
            Don_gia_moi = int(request.form.get('Th_Don_gia_Ban'))
            Tivi_Chon['Don_gia_Ban'] = Don_gia_moi
            Thong_bao = "Cập nhật thành công đơn giá bán mới là {:,}".format(Don_gia_moi).replace(",",".")
            Ghi_Tivi(Tivi_Chon)
        Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, Don_gia_moi)
        return render_template("Quan_ly_Ban_hang/MH_Cap_nhap_Tivi.html", Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)

@app.route("/Quan_ly_Ban_hang/Dang_xuat/",methods=['GET','POST'])
def QuanLyBanHangDangXuat():
    session.pop('quan_ly_ban_hang',None)
    return redirect(url_for('QuanLyBanHangDangNhap'))