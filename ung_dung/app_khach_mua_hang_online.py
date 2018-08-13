from flask import flash, redirect, render_template, request , session, abort, url_for, Markup
from ung_dung import app
from ung_dung.Xu_ly.Khach_mua_hang_Online.Xu_ly_3L import *
from ung_dung.Xu_ly.Khach_mua_hang_Online.Xu_ly_form import *
from datetime import datetime
@app.route("/khach-mua-hang-online", methods=['GET','POST'])
def KhachMuaHangOnline():
    Chuoi_HTML_Khach_hang = ""
    Chuoi_QL_Dang_nhap = ""
    if session.get('KHMH_online_Dang_nhap'):
        Khach_hang_Dang_nhap = session["KHMH_online_Dang_nhap"]
        Chuoi_HTML_Khach_hang = Tao_chuoi_HTML_Khach_hang(Khach_hang_Dang_nhap)        
    else: 
        Chuoi_QL_Dang_nhap = '<a href="/khach-mua-hang-online/Dang_nhap">Đăng nhập</a>'
        
# ****** Khởi động Dữ liệu Nguồn/Nội bộ ********    
    Danh_sach_Tivi_chon = []
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()   

 # ****** Khai báo Biến ********
    Chuoi_Tra_cuu="" # Biến Nhập liệu
    Danh_sach_Tivi_Xem = Danh_sach_Tivi # Biến Kết quả 

# ****** Nhập liệu và Xử lý nếu Hợp lệ ********  
    if (request.form.get('Th_Chuoi_Tra_cuu') !=None):
       Chuoi_Tra_cuu=request.form.get('Th_Chuoi_Tra_cuu')
       Danh_sach_Tivi_Xem= Tra_cuu_Tivi(Chuoi_Tra_cuu,Danh_sach_Tivi)
# xu ly them vao gio hang
    if request.method == 'POST':
        #them vao gio hang      
        if request.form.get('Th_Ma_so') !=None: 
            if session.get('Gio_hang'):
                Danh_sach_Tivi_chon = session['Gio_hang']['Gio_hang']
            
            Ma_so = request.form.get('Th_Ma_so')   
            So_luong = int(request.form.get("Th_So_luong"))  
            Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)
            if Lay_chi_tiet_Tivi(Danh_sach_Tivi_chon, Ma_so)!=None:
                #Tivi da co trong Danh_sach_Tivi_chon
                Tivi_cu = Lay_chi_tiet_Tivi(Danh_sach_Tivi_chon, Ma_so)
                So_luong_cu = Tivi_cu["So_luong"]
                So_luong = So_luong + So_luong_cu
                Danh_sach_Tivi_chon.remove(Tivi_cu)
            Tivi_Chon["So_luong"] = So_luong    
            Danh_sach_Tivi_chon.append(Tivi_Chon)
            session['Gio_hang'] = {'Gio_hang':Danh_sach_Tivi_chon}
        #cap nhat gio hang
        if request.form.get('Th_Ma_so_1') !=None: 
            Danh_sach_Tivi_chon = []
            if session.get('Gio_hang'):
                Danh_sach_Tivi_chon = session['Gio_hang']['Gio_hang']            
            Ma_so_1 = request.form.get('Th_Ma_so_1') 
            print("Ma so 1:", Ma_so_1)  
            So_luong_1 = int(request.form.get("Th_So_luong_1"))              
            Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi_chon, Ma_so_1)

            print("Tivi chọn:", Tivi_Chon)
            if Tivi_Chon!=None:
                Danh_sach_Tivi_chon.remove(Tivi_Chon)
            if So_luong_1>0 and Tivi_Chon!=None:
                Tivi_Chon['So_luong'] = So_luong_1
                Danh_sach_Tivi_chon.append(Tivi_Chon)
            session['Gio_hang'] = {'Gio_hang':Danh_sach_Tivi_chon}
    
    if session.get('Gio_hang'):
        Danh_sach_Tivi_chon = session['Gio_hang']['Gio_hang']
    Chuoi_HTML_Gio_hang = Tao_Chuoi_HTML_Danh_sach_Tivi_Gio_hang(Danh_sach_Tivi_chon)

# ****** Kết xuất  ********  
    Chuoi_HTML_Danh_sach_Tivi=Tao_Chuoi_HTML_Danh_sach_Tivi(
           Danh_sach_Tivi_Xem)

    Khung= render_template('Khach_mua_hang_Online/MH_Chinh.html', 
       Chuoi_Tra_cuu=Chuoi_Tra_cuu,
       Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi,
       Chuoi_HTML_Gio_hang = Chuoi_HTML_Gio_hang,
       Chuoi_HTML_Khach_hang = Chuoi_HTML_Khach_hang,
       Chuoi_QL_Dang_nhap = Markup(Chuoi_QL_Dang_nhap))
    return Khung

@app.route("/khach-mua-hang-online/Dang_nhap", methods=['GET', 'POST'])
def KHMHDang_nhap():
# ****** Khởi động Dữ liệu Nguồn/Nội bộ ********
    if session.get("KHMH_online_Dang_nhap"):
        return redirect(url_for('KhachMuaHangOnline'))
    Danh_sach_khach_hang = Doc_danh_sach_Khach_hang()
    Ten_dang_nhap = ""
    Mat_khau = ""
    Chuoi_Thong_bao = "Xin vui lòng Nhập Tên đăng nhập (email) và Mật khẩu"
    if request.method == 'POST':
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        Khach_hang = Dang_nhap_Khach_hang(Danh_sach_khach_hang, Ten_dang_nhap, Mat_khau)
        print(Khach_hang)
        Hop_le = (Khach_hang != None)
        if Hop_le:            
            session['KHMH_online_Dang_nhap'] = Khach_hang
            return redirect(url_for('KhachMuaHangOnline'))
        else:
            Chuoi_Thong_bao = "Đăng nhập không hợp lệ"
    Khung = render_template(
        'Khach_mua_hang_Online/MH_Dang_nhap.html',
        Chuoi_Thong_bao=Chuoi_Thong_bao)
    return Khung

@app.route("/khach-mua-hang-online/Dang_xuat", methods=['GET', 'POST'])
def KHMHDang_xuat():
    session.pop('KHMH_online_Dang_nhap', None)
    return redirect(url_for('KhachMuaHangOnline'))

@app.route("/khach-mua-hang-online/Dat_hang", methods=['GET', 'POST'])
def Dat_hang():
    Chuoi_QL_Dang_nhap =""
    Chuoi_HTML_Khach_hang = ""
    Chuoi_HTML_Gio_hang = ""
    Chuoi_HTML_Mua_hang = ""
    Chuoi_Thong_bao = ""
    Danh_sach_Tivi_chon = []
    if session.get('KHMH_online_Dang_nhap'):
        Khach_hang_Dang_nhap = session["KHMH_online_Dang_nhap"]
        Chuoi_HTML_Khach_hang = Tao_chuoi_HTML_Khach_hang(Khach_hang_Dang_nhap)    
        if session.get('Gio_hang'):
            Danh_sach_Tivi_chon = session['Gio_hang']['Gio_hang']
            Chuoi_HTML_Gio_hang = Tao_Chuoi_HTML_Danh_sach_Tivi_Gio_hang(Danh_sach_Tivi_chon)
            Chuoi_HTML_Mua_hang = Tao_Chuoi_HTML_Danh_sach_Tivi_Dat_hang(Danh_sach_Tivi_chon)   
            if request.method == 'POST':
                if request.form.get('Th_Dat_hang') =="DH_OK":
                # nguoi dung da nhan nut dat hang
                # ghi don hang vao CSDL
                    print(request.form.get('Th_Dat_hang'))
                    Don_hang = {}
                    Don_hang["Ngay_dat_hang"] = datetime.now().strftime('%d-%m-%Y')
                    Don_hang["Khach_hang"] = {"Khach_hang":Khach_hang_Dang_nhap}
                    Don_hang["Chi_tiet_don_hang"] = {"Chi_tiet_don_hang":Danh_sach_Tivi_chon}
                    print(Don_hang)
                    if Them_Don_hang(Don_hang):
                        Chuoi_Thong_bao = "<div>Đơn hàng của quý khách đã đặt thành công. <br/>"+\
                        "Cảm ơn quý khách đã ủng hộ cửa hàng.<br/>"+\
                        "<a href='/khach-mua-hang-online'>Tiếp tục mua hàng</a></div>"   
                        #giai phong gio hang
                        session.pop('Gio_hang', None)                            
                        Danh_sach_Tivi_chon = []
                        Chuoi_HTML_Mua_hang = ""   
                             
    else: 
        Chuoi_QL_Dang_nhap = '<div>Vui lòng <a href="/khach-mua-hang-online/Dang_nhap">Đăng nhập</a> để tiến hành đặt hàng<div>'
    
    Khung= render_template('Khach_mua_hang_Online/MH_Dat_hang.html', 
       Chuoi_HTML_Mua_hang=Chuoi_HTML_Mua_hang, 
       Chuoi_QL_Dang_nhap = Markup(Chuoi_QL_Dang_nhap),
       Chuoi_HTML_Khach_hang = Chuoi_HTML_Khach_hang,
       Chuoi_HTML_Gio_hang = Chuoi_HTML_Gio_hang,
       Chuoi_Thong_bao = Markup(Chuoi_Thong_bao))
    return Khung

@app.route("/khach-mua-hang-online/lien-he", methods=['GET', 'POST'])
def KH_Onlie_LH():
    thongbao=''
    form = Form_Lien_he(request.form)
    if form.validate_on_submit():
        Ho_ten = request.form['Th_Ho_ten']
        if request.form['Th_Gioi_tinh'] == 'M':
            Gioi_tinh = 'Nam'
        elif request.form['Th_Gioi_tinh'] == 'F':
            Gioi_tinh = 'Nữ'
        else:
            Gioi_tinh = 'Khác'
        Dia_chi = request.form['Th_Dia_chi']
        Email = request.form['Th_Email']
        Tuoi = request.form['Th_Tuoi']
        Ly_do = request.form['Th_Ly_do']
        Noi_dung = request.form['Th_Noi_dung']
        Lien_he={'Ho_ten':Ho_ten,'Gioi_tinh':Gioi_tinh,'Dia_chi':Dia_chi,\
        'Email':Email,'Tuoi':Tuoi,'Ly_do':Ly_do,'Noi_dung':Noi_dung}
        if Them_Lien_he(Lien_he):
            thongbao='Cảm ơn '+ Ho_ten +' đã gửi ý kiến'
    return render_template('Khach_mua_hang_Online/MH_Lien_he.html',form=form,thongbao=thongbao)

@app.route("/khach-mua-hang-online/dang-ky", methods=['GET', 'POST'])
def KH_Onlie_DK():
    thongbao=''
    form = Form_DK_TK(request.form)
    if form.validate_on_submit():
        Ho_ten = request.form['Th_Ho_ten']
        Email = request.form['Th_Email']
        Mat_khau = request.form['Th_Mat_khau']
        Xac_nhan = request.form['Th_Xac_nhan']
        Dia_chi = request.form['Th_Dia_chi']
        Dien_thoai = request.form['Th_Dien_thoai']
        Dia_chi_giao_hang=request.form['Th_Dia_chi_GH']
        Khach_hang={'Ho_ten':Ho_ten,'Email':Email,'Mat_khau':Mat_khau,'Dia_chi':Dia_chi,
        'Dien_thoai':Dien_thoai,'Dia_chi_giao_hang':Dia_chi_giao_hang}
        if Them_Khach_hang(Khach_hang):
            thongbao='Tài khoản của quý khách tạo thành công.'
    print(form.errors)
    return render_template('Khach_mua_hang_Online/MH_Dang_ky.html',form=form,thongbao=thongbao)