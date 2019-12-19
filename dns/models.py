from django.db import models
# Create your models here.


class Records(models.Model):
    id = models.AutoField(primary_key=True)
    zone = models.CharField(max_length=255,verbose_name="属于哪个Zone")
    host = models.CharField(max_length=255,verbose_name="二级域名")
    # dns_type = ((0,"A"),(1,"MX"),(2,"CNAME"),(3,"TXT"),(4,"NS"),(5,"SOA"),(6,"AAAA"),(7,"PTR"),)
    # type = models.SmallIntegerField(choices=dns_type,default=0,verbose_name="DNS类型")
    dns_type = models.CharField(max_length=16,null=True,verbose_name="DNS类型")
    data = models.CharField(max_length=255,verbose_name="对应的IP/值")
    ttl = models.IntegerField(default=60,verbose_name="生存周期时间")
    mx_priority = models.IntegerField(default=None)
    dns_view = ((0,"Telecom"),(1,'Unicom'),(2,"CMCC"),(3,"other"))
    view = models.SmallIntegerField(choices=dns_view,default=3,verbose_name="属于哪个公司")
    priority = models.IntegerField(default=255)
    refresh = models.IntegerField(default=28800)
    retry = models.IntegerField(default=14400)
    expire = models.IntegerField(default=86400)
    minimum = models.IntegerField(default=86400)
    serial = models.IntegerField(default=0)
    resp_person = models.CharField(max_length=64,default="test.com")
    primary_ns = models.CharField(max_length=64,default="ns.test.com.")

class ZoneRecords(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,verbose_name="属于哪个Zone",default="abc.com")