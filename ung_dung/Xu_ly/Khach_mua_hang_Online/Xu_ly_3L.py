from flask import   Markup, url_for
import json
import os
import sqlite3
Thu_muc_Du_lieu ="ung_dung/Du_lieu"
Thu_muc_Tivi = "ung_dung/Du_lieu/Tivi/"

# doc du_lieu tu CSDL
def Doc_bang_CSDL(Ten_bang):
    conn = sqlite3.connect("ung_dung/Du_lieu/ql_dat_hang.db")
    print(conn)
    print ("Opened database successfully")
    list_dong = []    
    cursor = conn.execute("select * from " +Ten_bang)
    for row in cursor:        
        print(row)
        list_dong.append(row)          
    print ("Operation done successfully")
    #print(list_dong)
    conn.commit()
    conn.close()
    return list_dong

def Doc_danh_sach_Khach_hang():
    Danh_sach = []    
    danh_sach_khach_hang = Doc_bang_CSDL("KHACH_HANG")
    #print(danh_sach_khach_hang)
    for KH in danh_sach_khach_hang:    
        KH_dict = {}
        KH_dict["ID"] = KH[0]
        KH_dict["Ho_ten"] = KH[1]
        KH_dict["Email"] = KH[2]
        KH_dict["Mat_khau"] = KH[3]
        KH_dict["Dia_chi"] = KH[4]
        KH_dict["Dien_thoai"] = KH[5]
        KH_dict["Dia_chi_giao_hang"] = KH[6]
        Danh_sach.append(KH_dict)
    return Danh_sach

# Xử lý Lưu trữ 
def Doc_Danh_sach_Tivi():
    Danh_sach = []
    for Ten_Tap_tin in os.listdir(Thu_muc_Tivi):
        Duong_dan = Thu_muc_Tivi + Ten_Tap_tin  
        data_file = open(Duong_dan, encoding='utf-8')    
        Tivi = json.load(data_file)    
        data_file.close()
        Danh_sach.append(Tivi)   
    return Danh_sach

def Them_Khach_hang(Khach_hang):
    result = False
    conn = sqlite3.connect("ung_dung/Du_lieu/ql_dat_hang.db")
    sql = "INSERT INTO KHACH_HANG (Ho_ten,Email,Mat_khau, Dia_chi,Dien_thoai,Dia_chi_giao_hang) \
                  VALUES (?, ?, ?, ?, ?, ?)"
    if conn.execute(sql,(Khach_hang["Ho_ten"], Khach_hang["Email"], Khach_hang["Mat_khau"],\
                     Khach_hang["Dia_chi"], Khach_hang["Dien_thoai"], Khach_hang["Dia_chi_giao_hang"])):
        print('Khach hang is inserted successfully!')
        result = True
    conn.commit()    
    conn.close()
    return result

def Them_Don_hang(Don_hang):
    result = False
    conn = sqlite3.connect("ung_dung/Du_lieu/ql_dat_hang.db", timeout=10)
    sql = "INSERT INTO DON_HANG(Ngay_dat_hang,Khach_hang,Chi_tiet_don_hang) \
                  VALUES (?, ?, ?)"
    Khach_hang = json.dumps(Don_hang["Khach_hang"],ensure_ascii=False)
    Chi_tiet_don_hang = json.dumps(Don_hang["Chi_tiet_don_hang"],ensure_ascii=False)
    if conn.execute(sql,(Don_hang["Ngay_dat_hang"],Khach_hang,Chi_tiet_don_hang)):
        print('Don_hang is inserted successfully!')
        result = True
    conn.commit()    
    conn.close()
    return result
	
def Them_Lien_he(Lien_he):
    result = False
    conn = sqlite3.connect("ung_dung/Du_lieu/ql_dat_hang.db")
    sql = "INSERT INTO LIEN_HE(Ho_ten,Gioi_tinh,Dia_chi,Email,Tuoi,Ly_do,Noi_dung) \
                  VALUES (?, ?, ?, ?, ?, ?, ?)"
    if conn.execute(sql,(Lien_he["Ho_ten"],Lien_he["Gioi_tinh"],Lien_he["Dia_chi"],\
				Lien_he["Email"],Lien_he["Tuoi"],Lien_he["Ly_do"],Lien_he["Noi_dung"])):
        print('Don_hang is inserted successfully!')
        result = True
    conn.commit()    
    conn.close()
    return result

# Xử lý Nghiệp vụ 
def Tra_cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi):
    Danh_sach=list(filter(
        lambda Tivi: Chuoi_Tra_cuu.upper() in  Tivi["Ten"].upper(),Danh_sach_Tivi))
    return Danh_sach
#lay chi tiet tivi
def Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so):
    Danh_sach  = list(filter(
        lambda Tivi: Tivi["Ma_so"] == Ma_so, Danh_sach_Tivi
    ))
    Tivi = Danh_sach[0] if len(Danh_sach)==1 else None

    return Tivi

# lay thong tin NV
def Dang_nhap_Khach_hang(Danh_sach_Khach_hang, Ten_dang_nhap, Mat_khau):
    Danh_sach = list(filter(
        lambda Khach_hang: Khach_hang['Email'] == Ten_dang_nhap and Khach_hang["Mat_khau"] == Mat_khau
        , Danh_sach_Khach_hang))
    khach_hang = Danh_sach[0] if len(Danh_sach)==1 else None
    
    return khach_hang

# Xử lý Thể hiện
def Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi):
    Chuoi_HTML_Danh_sach = '<div class="row" >'
    for Tivi in Danh_sach_Tivi:
        Chuoi_Don_gia_Ban="Đơn giá Bán {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".")    
        Chuoi_Hinh_nho='<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
        Chuoi_Hinh_to='<img  style="width:300px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
        Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
        Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 Tivi["Ten"] + "<br />" + Chuoi_Don_gia_Ban + "</div>"
        
        Chuoi_form =  '''<div><form method="post" action="/khach-mua-hang-online">            
                <input type="hidden" name="Th_Ma_so" value="'''+Tivi["Ma_so"]+'''"/>
                <input type="number" style="width:60px" name="Th_So_luong" value="1" min="1" max="'''+str(Tivi["So_luong_Ton"])+'''"/>
                <button class="btn btn-primary" type="submit">Chọn</button>
                </form></div>'''
        
        Chuoi_HTML ='<div class="col-md-4" >' +  \
                Chuoi_Hinh_nho + Chuoi_Thong_tin + Chuoi_form+ '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  

def Tao_Chuoi_HTML_Danh_sach_Tivi_Gio_hang(Danh_sach_Tivi):
    Chuoi_HTML_Danh_sach = '<div class="row">'
    Chuoi_HTML_Danh_sach +='<div class="btn TOM_TAT" style="color:blue"> &nbsp;&nbsp;&nbsp;Chi tiết giỏ hàng</div>'
    Chuoi_HTML_Danh_sach +='<div class="container">'
    for Tivi in Danh_sach_Tivi:
        Chuoi_Don_gia_Ban="Đơn giá Bán {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".")    
        Chuoi_Hinh_nho='<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
        
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 Tivi["Ten"] + "<br />" + Chuoi_Don_gia_Ban + "</div>"
        
        Chuoi_form =  '''<div ><form method="post" action="/khach-mua-hang-online">            
                <input type="hidden" name="Th_Ma_so_1" value="'''+Tivi["Ma_so"]+'''"/>
                <input type="number" name="Th_So_luong_1" value="'''+str(Tivi["So_luong"])+'''" min="0" max="'''+str(Tivi["So_luong_Ton"])+'''"/>
                <button class="btn btn-primary" type="submit">Cập nhật</button>
                </form></div>'''
        
        Chuoi_HTML ='<div class="col-md-12" >' +  \
                Chuoi_Hinh_nho + Chuoi_Thong_tin + Chuoi_form+ '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach +="</div>"

    Chuoi_Dat_hang = '''<div style="width:80%; text-align:right"><form method="post" action="/khach-mua-hang-online/Dat_hang">  
                 &nbsp;&nbsp;&nbsp;<button class="btn btn-success" type="submit">Tiến hành đặt hàng</button>
                </form></div>'''

    Chuoi_HTML_Danh_sach += Chuoi_Dat_hang + '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  

def Tao_Chuoi_HTML_Danh_sach_Tivi_Dat_hang(Danh_sach_Tivi):
    Tong_so_tien = 0
    Chuoi_HTML_Danh_sach = '<div class="row">'
    Chuoi_HTML_Danh_sach +='<div class="btn TOM_TAT" style="color:blue"> &nbsp;&nbsp;&nbsp;ĐƠN HÀNG<br/>Chi tiết đơn hàng</div>'    
    Chuoi_HTML_Danh_sach +='<div class="container">'
    for Tivi in Danh_sach_Tivi:
        Chuoi_Don_gia_Ban="Đơn giá Bán: {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".")    
        Chuoi_Hinh_nho='<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
        Thanh_tien = Tivi["So_luong"] * Tivi["Don_gia_Ban"]
        Tong_so_tien += Thanh_tien
        Chuoi_thanh_tien = "Thành tiền:" +str(Tivi["So_luong"]) +"x" + \
                            "{:,}".format(Tivi["Don_gia_Ban"]).replace(",",".") + " = " +\
                            "{:,}".format(Thanh_tien).replace(",",".")
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 Tivi["Ten"] + "<br />" + Chuoi_Don_gia_Ban + "<br/>" + Chuoi_thanh_tien + "</div>"
        
        Chuoi_HTML ='<div>' +  \
                Chuoi_Hinh_nho + Chuoi_Thong_tin + '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach +="</div>"
    Chuoi_Tong_tien="<br/>Tổng tiền {:,}".format(Tong_so_tien).replace(",",".")
    Chuoi_HTML_Danh_sach +="<div>" + Chuoi_Tong_tien + "</div>"

    Chuoi_Dat_hang = '''<br/><div ><form method="post" action="/khach-mua-hang-online/Dat_hang"> 
                <input type="hidden" name="Th_Dat_hang" value="DH_OK"/>                               
                 &nbsp;&nbsp;&nbsp;<button class="btn btn-success" type="submit">Đặt hàng</button>
                </form></div>'''

    Chuoi_HTML_Danh_sach += Chuoi_Dat_hang + '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  

def Tao_chuoi_HTML_Khach_hang(Khach_hang):    
    Chuoi_HTML_Khach_hang = '<div class="row" >'
    Chuoi_Hinh = '<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = 'NV_1.png') + '" />'
    Chuoi_Thong_tin = '<div class="btn" style="text-align:left"> Xin chào quý khách ' + \
                 Khach_hang["Ho_ten"] + "</div>"    
    Chuoi_HTML_Khach_hang += Chuoi_Hinh + Chuoi_Thong_tin + '</div><a href="/khach-mua-hang-online/Dang_xuat">Đăng xuất</a>'    
    return Markup(Chuoi_HTML_Khach_hang)  
 