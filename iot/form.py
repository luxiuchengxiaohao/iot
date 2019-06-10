from django import forms
from django.core.exceptions import ValidationError
import re
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|14[0-9]|15[0-9]|16[0-9]|17[0-9]|18[0-9]|19[0-9])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')
class verifycode_form(forms.Form):
    n = forms.CharField(validators=[mobile_validate, ],required=True, error_messages={'required': "手机号不能为空。"})
class registerForm(forms.Form):
    # username = forms.CharField(max_length=24,min_length=3,required=True,error_messages={'required': "账号不能为空。",'min_length': "账号至少为3位",'max_length':"账号最长为24位"})
    password = forms.CharField(max_length=96,min_length=8,required=True,error_messages={'required':  "密码不能为空。",'min_length': "密码至少为8位",'max_length':"密码最长为96位"})
    username = forms.CharField(validators=[mobile_validate, ],required=True,error_messages={'required':  "手机号不能为空。"})
    type = forms.IntegerField(max_value=1,min_value=0,required=True,error_messages={'required':  "type参数不能为空。",'min_length': "type参数错误！",'max_length':"type参数错误！"})
class loginForm(forms.Form):
    # username = forms.CharField(max_length=24,min_length=3,required=True,error_messages={'required': "账号不能为空。",'min_length': "账号至少为3位",'max_length':"账号最长为24位"})
    password = forms.CharField(max_length=96,min_length=8,required=True,error_messages={'required':  "密码不能为空。",'min_length': "密码至少为8位",'max_length':"密码最长为96位"})
    username = forms.CharField(validators=[mobile_validate, ],required=True,error_messages={'required':  "手机号不能为空。"})
