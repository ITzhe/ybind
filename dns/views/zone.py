from dns import models
from django.views import View
from django.shortcuts import render, HttpResponse,redirect


# Create your views here.

class Zone(View):
    def get(self, request):
        ret = models.ZoneRecords.objects.only('title')
        return render(request, 'zone_list.html', {"zone_list": ret})


class ZoneAdd(View):
    def get(self, request):
        return render(request, 'zone_add.html')

    def post(self, request):
        domain = request.POST.get('domain')
        ret = models.ZoneRecords.objects.filter(title=domain)
        if ret:
            return HttpResponse("此域名已经存在！！！")

        zone_list = models.ZoneRecords.objects.values('title')

        # 生成view_Title
        zone_file = open("view.conf", "w")
        zone_file.write('''view "View" { \n''')
        zone_file.close()

        # 重新生成新的view文件
        for zone in zone_list:
            zone = list(zone.values())[0]
            zone_info = '''  zone "%s" {\n\ttype    master;\n\tfile  "%s.zone";\n  };\n''' % (zone, zone)
            # 循环打开文件追加到文件结尾
            zone_file = open("view.conf", "a")
            zone_file.write(zone_info)
            zone_file.close()


        # 将用户输入记录到数据库
        models.ZoneRecords.objects.create(title=domain)

        # 将用户输入的添加到view文件结尾
        zone_info = '''  zone "%s" {\n\ttype    master;\n\tfile  "%s.zone";\n  };\n};''' % (domain, domain)
        with open("view.conf", "a") as f:
            f.write(zone_info)

        return redirect("/zone-list/")



    def delete(self, request,id):
        # 从数据库删除记录
        models.ZoneRecords.objects.filter(id=id).delete()

        # 重新生成配置文件
        zone_list = models.ZoneRecords.objects.values('title')

        # 生成view_Title
        zone_file = open("view.conf", "w")
        zone_file.write('''view "View" { \n''')
        zone_file.close()

        # 重新生成新的view文件
        for zone in zone_list:
            zone = list(zone.values())[0]
            zone_info = '''  zone "%s" {\n\ttype    master;\n\tfile  "%s.zone";\n  };\n''' % (zone, zone)
            # 循环打开文件追加到文件结尾
            zone_file = open("view.conf", "a")
            zone_file.write(zone_info)
            zone_file.close()

        with open("view.conf", "a") as f:
            f.write("};")

        return redirect("/zone-list/")

