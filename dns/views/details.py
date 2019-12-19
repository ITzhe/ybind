from dns import models
from django.db.models import Q
from django.db.models import F

from django.views import View
from django.shortcuts import render, HttpResponse, redirect


# def DetailsList(request, domain):
#     print(domain)
#     dns_list = models.Records.objects.filter(zone=domain)
#     for d in dns_list:
#         print(d)
#     return render(request, "detail_list.html", {"dns_list": dns_list})


class Details(View):
    def get(self, request, domain):
        dns_list = models.Records.objects.filter(zone=domain)
        return render(request, "detail_list.html", {"dns_list": dns_list, "domain": domain})


class DetailAdd(View):
    def get(self, request, domain):
        return render(request, "detail-add.html", {"domain": domain})

    def post(self, request, domain):
        # domain = request.POST.get('domain')
        d_type = request.POST.get('type')
        host = request.POST.get('host')
        data = request.POST.get('data')
        ipt_mx = request.POST.get('ipt_mx')
        ttl = request.POST.get('ttl')

        ret = models.Records.objects.filter(zone=domain,host=host).values_list()
        if ret:
            return HttpResponse("此域名已经存在！！！")

        if d_type != "MX":
            ipt_mx = 0

        models.Records.objects.create(
            zone=domain,
            dns_type=d_type,
            host=host,
            data=data,
            ttl=ttl,
            mx_priority=ipt_mx,
        )

        # 使 serial 号 + 1
        ser = models.Records.objects.filter(zone=domain).first()
        serial_number = ser.serial + 1
        minimum_number = ser.minimum
        expire_number = ser.expire
        retry_number = ser.retry
        refresh_number = ser.refresh

        models.Records.objects.filter(zone=domain).update(serial=serial_number)

        detail_records = models.Records.objects.filter(zone=domain)

        # 生成Zone文件
        Title = f'''$TTL 1D
$ORIGIN {domain}.
@   IN SOA  @ {domain}. (
   {serial_number}   ; serial
   {refresh_number}  ; refresh
   {retry_number}  ; retry
   {expire_number}  ; expire
   {minimum_number} ); minimum'''

        zone_file = open(f"{domain}.zone", "w")
        zone_file.write(f'''{Title}\n''')
        zone_file.close()

        # 重新生成新的zone文件
        # www A	1.1.1.1
        for detail in detail_records:
            zone_info = f'{detail.host}\t{detail.dns_type}\t{detail.data}\n'
            # 循环打开文件追加到文件结尾
            zone_file = open(f"{domain}.zone", "a")
            zone_file.write(zone_info)
            zone_file.close()

        return redirect("/detail/%s/" %(domain))


class BatchAdd(View):
    def get(self, request):
        zone_list = models.ZoneRecords.objects.all()
        return render(request, "batch_add.html",{"zone_list":zone_list})