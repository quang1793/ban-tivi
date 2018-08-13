from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField
from wtforms import validators, ValidationError

class Form_Lien_he(Form):
    Th_Ho_ten   = TextField('Tên khách hàng',[validators.required('Phải nhập tên khách hàng')])
    Th_Gioi_tinh= RadioField('Giới tính', choices=[('M', 'Nam'),('F','Nữ'),('D','Khác')], default='D')
    Th_Dia_chi  = TextField('Địa chỉ',[validators.required('Phải nhập địa chỉ')])
    Th_Email    = TextField('Email', [validators.Email('Email không hợp lệ')])
    Th_Tuoi     = IntegerField('Tuổi', [validators.required('Phải nhập tuổi')])
    Th_Ly_do    = SelectField('Góp ý cho', choices=[('TGGH','Thời gian giao hàng'),
        ('CSKH','Chăm sóc khách hàng'),('BHSP','Bảo hành sản phẩm')])
    Th_Noi_dung = TextAreaField('Nội dung', [validators.required('Phải nhập nội dung')])
    Th_submit   = SubmitField('Gửi ý kiến')

class Form_DK_TK(Form):
    Th_Ho_ten     = TextField('Tên khách hàng',[validators.required('Phải nhập tên khách hàng')])
    Th_Email      = TextField('Email', [validators.Email('Email không hợp lệ')])
    Th_Mat_khau   = PasswordField('Password', [
        validators.required('Vui lòng nhập mật khẩu.'),
        validators.length(min=6, message='Mật khẩu có ít nhất 6 ký tự.'),
        validators.EqualTo('Th_Xac_nhan', message='Mật khẩu phải trùng khớp.')
    ])
    Th_Xac_nhan   = PasswordField('Lặp lại mật khẩu.')
    Th_Dia_chi    = TextField('Địa chỉ',[validators.required('Phải nhập địa chỉ')])
    Th_Dien_thoai = IntegerField('Điện thoại',[validators.required('Phải nhập số điện thoại.')])
    Th_Dia_chi_GH = TextAreaField('Địa chỉ giao hàng', [validators.required('Phải nhập Địa chỉ giao hàng')])
    Th_submit_dk     = SubmitField('Đăng ký')