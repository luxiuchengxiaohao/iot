from django.db import models
from django.contrib import admin
# class user(admin.AdminSite):
#     pass
class user(models.Model):
    username = models.CharField(max_length=11)
    password = models.CharField(max_length=96)
    api_key = models.CharField(max_length=16)
    api_secret = models.CharField(max_length=32)
    regist_datetime = models.DateTimeField()
    last_login_datetime = models.DateTimeField()
    login_numbers = models.IntegerField()
class devices(models.Model):
    device_type = models.IntegerField()
    device_id = models.CharField(max_length=16)
    device_name = models.CharField(max_length=32)
    sn_code = models.CharField(max_length=128)
    key = models.CharField(max_length=128)
    bind_user = models.CharField(max_length=11)
    group = models.IntegerField()
    add_datetime = models.DateTimeField()
    last_register_datetime = models.DateTimeField()
    register_count = models.IntegerField()

