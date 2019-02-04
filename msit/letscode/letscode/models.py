from django.db import models
from django.db import utils


class users(models.Model):
    uemail = models.CharField(max_length=50,primary_key=True)
    pwd = models.CharField(max_length=50)
    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    umob = models.CharField(max_length=50)
    ugen = models.CharField(max_length=50)
    urole = models.CharField(max_length=50)

def unicode(self):
    return u'%s,%s,%s,%s,%s,%s,%s'%(self.uemail,self.pwd,self.uid,self.uname,self.umob,self.ugen,self.urole)
