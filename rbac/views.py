from rbac import models
from django.views import View
from django.shortcuts import render, HttpResponse, redirect


class Login(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        name = request.POST.get("username")
        password = request.POST.get("password")
        obj = models.UserInfo.objects.filter(name=name, password=password).first()
        if not obj:
            return HttpResponse("用户名或者密码错误")

        role = obj.roles.all()  # 查询当前用户的所有角色
        permissions_list = []  # 空列表，用来存放用户能访问的url列表

        for i in role:  # 循环角色
            per = i.permissions.all()  # 查看当前用户所有角色的所有权限
            # print(i.permissions.all())
            for j in per:
                # print(j.url)
                # 将所有授权的url添加到列表中
                permissions_list.append(j.url)

        request.session['url'] = permissions_list

        return redirect("/zone-list/")