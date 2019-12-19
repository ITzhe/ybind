from rbac import models
from django.contrib import admin


# Register your models here.
admin.site.register(models.Permission)
admin.site.register(models.Role)
admin.site.register(models.UserInfo)