from flask import flash, redirect, render_template, request, session, abort, url_for, Markup
from werkzeug.utils import secure_filename
from ung_dung import app
from ung_dung.Xu_ly.Quan_ly_Cong_ty.Xu_ly_3L import * 

'''app = Flask(__name__, static_url_path="",static_folder="Media",template_folder="Giao_dien")
app.secret_key="super secret key"'''

UPLOAD_FOLDER = app.static_folder
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/quan-ly-cong-ty/dang-nhap", methods=['GET', 'POST'])
def QLCT_Dang_nhap():
    if (session.get('Quan_ly_cong_ty_Dang_nhap')):
        return redirect(url_for('QLCT_Danh_sach_tivi'))
    Cong_ty = Doc_Cong_ty()
    Ten_dang_nhap=''
    Mat_khau=''
    Chuoi_Thong_bao = 'Xin vui lòng nhập tên đăng nhập và mật khẩu'
    if (request.method == "POST"):
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty['Danh_sach_Quan_ly_Cong_ty'],Ten_dang_nhap,Mat_khau)
        if (Nhan_vien != None):
            session['Quan_ly_cong_ty_Dang_nhap'] = Nhan_vien
            return redirect(url_for('QLCT_Danh_sach_tivi'))
        else:
            Chuoi_Thong_bao = 'Đăng nhập không hợp lệ'
    return render_template('Quan_ly_Cong_ty/MH_Dang_nhap.html', Chuoi_Thong_bao=Chuoi_Thong_bao,\
    Ten_dang_nhap=Ten_dang_nhap, Mat_khau=Mat_khau)

@app.route("/quan-ly-cong-ty/danh-sach-tivi", methods=['GET', 'POST'])
def QLCT_Danh_sach_tivi():
    Nhan_vien_Dang_nhap = session['Quan_ly_cong_ty_Dang_nhap']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)
    Dia_chi_MH = "/Quan_ly_Cong_ty/Xem_Danh_sach_Tivi"
    Chuoi_Tra_cuu=''

    if (request.method == 'POST'):
        Ma_so = request.form.get('Th_Ma_so')
        if (Ma_so == 'DANH_SACH'):
            Dia_chi_MH = '/Quan_ly_Cong_ty/Xem_Danh_sach_Tivi'
        if (Ma_so == 'TRA_CUU' and request.form.get('Th_Chuoi_Tra_cuu')!=''):
            Chuoi_Tra_cuu = request.form.get('Th_Chuoi_Tra_cuu')
            Dia_chi_MH = '/Quan_ly_Cong_ty/Tra_cuu/' + Chuoi_Tra_cuu + '/'
        if (Ma_so == 'SO_LUONG_TON'):
            Dia_chi_MH = '/Quan_ly_Cong_ty/Thong_ke/'
        if (Ma_so == 'DOANH_THU_TIVI'):
            Dia_chi_MH = '/Quan_ly_Cong_ty/Thong_ke_Doanh_thu'
        if (Ma_so == 'DOANH_THU_NHAN_VIEN'):
            Dia_chi_MH = '/Quan_ly_Cong_ty/Thong_ke_Doanh_thu_Nhan_vien'
        if (Ma_so == 'THEM_TIVI'):
            Dia_chi_MH = '/Quan_ly_Cong_ty/Them_Tivi'
    return render_template('/Quan_ly_Cong_ty/MH_Chinh.html',Dia_chi_MH=Dia_chi_MH,
    Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien, Chuoi_Tra_cuu=Chuoi_Tra_cuu)

def Thong_tin():
    Nhan_vien_Dang_nhap = session["Quan_ly_cong_ty_Dang_nhap"]
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    return Chuoi_HTML_Nhan_vien, Danh_sach_Tivi


@app.route("/Quan_ly_Cong_ty/Xem_Danh_sach_Tivi", methods=['GET', 'POST'])
def QLCT_Xem_Danh_sach_Tivi():    
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
 # ****** Khai báo Biến ********
    Danh_sach_Tivi_Xem = Danh_sach_Tivi # Biến Kết quả
# ****** Kết xuất  ********
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(
        Danh_sach_Tivi_Xem)
    Khung = render_template('Quan_ly_Cong_ty/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien,
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)
    return Khung

@app.route("/Quan_ly_Cong_ty/Tra_cuu/<string:Chuoi_Tra_cuu>/", methods=['GET', 'POST'])
def QLCT_Tra_cuu_Tivi_theo_Chuoi_Tra_cuu(Chuoi_Tra_cuu):
    print('Cần phải vào đây: ', Chuoi_Tra_cuu)
    # ****** Khởi động Dữ liệu Nguồn/Nội bộ ********
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
 # ****** Khai báo Biến ********
    Danh_sach_Tivi_Xem = Danh_sach_Tivi
    # Biến Kết quả
    Danh_sach_Tivi_Xem = Tra_cuu_Tivi(
        Chuoi_Tra_cuu, Danh_sach_Tivi)

# ****** Kết xuất  ********
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(
        Danh_sach_Tivi_Xem)
    Khung = render_template('Quan_ly_Cong_ty/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_Tra_cuu=Chuoi_Tra_cuu, Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien,
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)
    return Khung

@app.route("/Quan_ly_Cong_ty/Thong_ke/", methods=['GET', 'POST'])
def QLCT_Thong_ke_SL_ton():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    Cong_ty = Doc_Cong_ty()
    Danh_sach_Nhom_Tivi = Cong_ty["Danh_sach_Nhom_Tivi"]

    Danh_sach_Thong_ke = Thong_ke_So_luong_Ton(Danh_sach_Nhom_Tivi, Danh_sach_Tivi)
    
    Chuoi_HTML_Thong_ke_Tivi =  Tao_Chuoi_HTML_Thong_ke_SL_Ton_Tivi(Danh_sach_Thong_ke)
    return render_template(
        'Quan_ly_Cong_ty/MH_Xem_SL_Ton.html', Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route("/Quan_ly_Cong_ty/Thong_ke_Doanh_thu", methods=['GET', 'POST'])
def QLCT_Thong_ke_Doanh_thu():       
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)
    
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_ban, Ngay)
    

    Chuoi_HTML_Thong_ke_Tivi =  Tao_Chuoi_HTML_Thong_ke_Doanh_thu_Tivi(Danh_sach_Thong_ke)   
    return render_template(
            'Quan_ly_Cong_ty/MH_Xem_Doanh_thu_Tivi.html', Chuoi_HTML_Thong_ke_Tivi = Chuoi_HTML_Thong_ke_Tivi)

@app.route("/Quan_ly_Cong_ty/Thong_ke_Doanh_thu_Nhan_vien", methods=['GET', 'POST'])
def QLCT_Thong_ke_Doanh_thu_Nhan_vien():       
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)
    
    Chuoi_HTML_Thong_ke_Nhan_vien = Tao_Chuoi_HTML_Thong_ke_Doanh_thu_Nhan_vien(Danh_sach_Tivi_ban)
    
    return render_template(
            'Quan_ly_Cong_ty/MH_Xem_Doanh_thu_Nhan_vien.html', Chuoi_HTML_Thong_ke_Nhan_vien = Chuoi_HTML_Thong_ke_Nhan_vien)


@app.route("/Quan_ly_Cong_ty/Dang_xuat/", methods=['GET', 'POST'])
def QLCT_Dang_xuat():
    session.pop('Quan_ly_cong_ty_Dang_nhap', None)
    return redirect(url_for('QLCT_Dang_nhap'))

@app.route('/Quan_ly_Cong_ty/Them_Tivi',methods=['GET','POST'])
def Them_Tivi_moi():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    Cong_ty = Doc_Cong_ty()
    Danh_sach_nhom_Tivi = Cong_ty["Danh_sach_Nhom_Tivi"]

    Chuoi_HTML_select = Tao_Chuoi_HTML_Select_Nhom_Tivi(Danh_sach_nhom_Tivi)

    Chuoi_Thong_bao = ''
    Hinh_mac_dinh = 'TIVI_default.png'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # lay tap tin mac dinh
            flash('No file part')
            Chuoi_Thong_bao = "Vui lòng chọn hình"
        #    return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
        #    return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("file name:", filename)
            Hinh_mac_dinh = str(filename)
            Chuoi_Thong_bao = 'Đã thêm Tivi'
            #return redirect(url_for('Them_Tivi_moi', filename=filename))
        # check for tivi infromation
        Ten_dang_nhap = ""
        Mat_khau = ""
        Chuoi_Thong_bao = "Xin vui lòng Nhập các thông tin liên quan tới Tivi"               
          
        Hop_le = (request.form.get('Th_Ten')!=None and request.form.get('Th_Ky_hieu')!=None)
        if Hop_le:
            Ten = request.form.get('Th_Ten')
            So = max(Doc_Danh_sach_Ma_So_Hinh(Danh_sach_Tivi)) + 1 
            Ma_so = "TIVI_" +str(So)
            Ky_hieu = request.form.get('Th_Ky_hieu')    
            Don_gia_Ban = int(request.form.get("Th_Don_gia_Ban"))       
            Don_gia_Nhap = int(request.form.get("Th_Don_gia_Nhap"))  
            So_luong_Ton = int(request.form.get("Th_So_luong_Ton")) 
            Ma_Nhom_Tivi = request.form.get("Th_Ma_so")
            Ten_nhom = Lay_Nhom_Tivi(Ma_Nhom_Tivi, Danh_sach_nhom_Tivi) 
            TIVI = {"Ten":Ten,
            "Ma_so":Ma_so,
            "Ky_hieu":Ky_hieu,
            "Don_gia_Ban":Don_gia_Ban,
            "Don_gia_Nhap":Don_gia_Nhap,
            "So_luong_Ton":So_luong_Ton,
            "Danh_sach_Phieu_Ban":[],
            "Danh_sach_Phieu_Nhap":[],
            "Nhom_Tivi":{"Ten":Ma_Nhom_Tivi,"Ma_so":Ten_nhom}}
            if Ghi_Tivi(TIVI):
                # doi ten tap tin hinh filename => Ma_so.png
                os.rename(UPLOAD_FOLDER + '/' +filename, UPLOAD_FOLDER + '/' + Ma_so + ".png")
                print("doi ten ok")
            Chuoi_Thong_bao = "Đã thêm tivi"
        else:
            Chuoi_Thong_bao = "Thông tin không hợp lệ" 
            
    return render_template('Quan_ly_Cong_ty/MH_Them_tivi.html',Chuoi_Nhom_Tivi=Chuoi_HTML_select, 
    Chuoi_Thong_bao=Chuoi_Thong_bao)
    