from django.test import TestCase

# Create your tests here.


import re
import os

if __name__ == "__main__":
    # 设置django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ybind.settings")
    import django
    django.setup()

    from rbac import models

    # 固定用户名和密码
    user = 'admin'
    pwd = '123456'

    obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
    role = obj.roles.all()  # 查询当前用户的所有角色
    permissions_list = []  # 空列表，用来存放用户能访问的url列表


    for i in role:  # 循环角色
        per = i.permissions.all()  # 查看当前用户所有角色的所有权限
        # print(i.permissions.all())
        for j in per:
            # print(j.url)
            # 将所有授权的url添加到列表中
            permissions_list.append(j.url)



    print(permissions_list)


