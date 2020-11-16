# coding=utf-8

"""
Author: Yao Zhao
Create Date: 2020-10-14
@Software: Pycharm
"""

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# 注册form认证
class RegForm(forms.Form):
    """定义注册帐号的form组件"""
    username = forms.CharField(
        label = "Username",
        max_length=18,
        error_messages={
            "required":"Content cannot be empty",
            "invalid":"Invalid format",
            "max_length":"The user name the longest do not exceed 18"
        },
        widget=forms.TextInput(attrs={"class":"forms-control"})
    )

    password = forms.CharField(
        min_length=6,
        error_messages={
            "required": "Content cannot be empty",
            "invalid": "Invalid format",
            "min_length": "The password may not be less than 6"
        }
    )

    r_password = forms.CharField(
        min_length=6,
        error_messages={
            "required": "Content cannot be empty",
            "invalid": "Invalid format",
            "min_length": "The password may not be less than 6"
        }
    )

    email = forms.CharField(
        label="邮箱",
        error_messages={
            "required": "Content cannot be empty",
            "invalid": "Invalid format",
        },
        validators=[RegexValidator(r"^\w+@\w+\.com$", "邮箱格式不正确")]
    )

    # phone = forms.CharField(
    #     label="电话",
    #     error_messages={
    #         "required": "Content cannot be empty",
    #         "invalid": "Invalid format",
    #     },
    #     validators=[RegexValidator(r"^[0-9]{4,11}$","请输入正确的号码")]
    # )

    # 定义局部钩子
    def clean_password(self):
        # 校验密码的合法性，不能为纯数据
        password = self.cleaned_data.get("password")
        if password.isdecimal():
            raise ValidationError("Password cannot be pure digital!")
        return password

    def clean_r_password(self):
        # 校验密码的合法性，不能为纯数据
        r_password = self.cleaned_data.get("r_password")
        if r_password.isdecimal():
            raise ValidationError("Password cannot be pure digital！")
        return r_password

    # 定义全局钩子
    def clean(self):
        # 校验两次密码输入是否一致
        if self.cleaned_data.get("password") != self.cleaned_data.get("r_password"):
            self.add_error("r_password","Two password input inconsistent!")
        else:
            return self.cleaned_data

    # 重写init方法，来批量设置标签的样式
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"forms-control"})
