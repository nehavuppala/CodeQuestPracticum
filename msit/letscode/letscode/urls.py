"""letscode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from . import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home.my, name="home"),
    path('log', home.log, name="log"),
    path('questIn', home.questIn, name="questIn"),
    url('mtest', home.mtest, name="test"),
    url('mhome', home.mhome, name='home'),
    url('viewQuestions', home.viewQuestions, name='viewq'),
    url('ctext', home.ctext, name="ctext"),
    path('testin', home.testin, name="testin"),
    url('viewTests', home.viewTests, name="vtest"),
    url('logout', home.logout, name="out"),
    url('shome', home.shome, name="shome"),
    url('satest', home.satest, name='satest'),
    path('takeTest', home.takeTest, name='takeTest'),
    path('execute', home.execute, name="execute"),
    url('qedit', home.qedit, name='edits'),
    path('editform', home.editform, name="editform"),
    path('qed', home.qed, name="qedit2"),
    url('etest', home.etest, name="etest"),
    path('teform', home.teform, name="teform"),
    url('qdel', home.qdel, name="qdel"),
    path('questdel', home.questdel, name="questdel"),
    path('tediting', home.tediting, name="tediting"),
    url('tdel', home.tdel, name='tdel'),
    path('tdl', home.tdl, name='tdl'),
    path('adminhome', home.adminhome, name='adminhome'),
    path('list', home.list, name='list'),
    path('upload', home.upload, name='upload'),
    path('dataupload', home.dataupload, name='dataupload'),
    url('results', home.results, name="res"),
    url('sres', home.sres, name='sres'),
    path('srt', home.srt, name='srt'),
    url('bdelete', home.bdelete, name='bdel'),
    path('delbat', home.delbat, name='delbat'),
    path('updres', home.updres, name='updres'),
    url('groups', home.groups, name='cgroup'),
    path('cgp', home.cgp, name='cgp'),
    path('cregroup', home.cregroup, name='cregroup'),
    path('ausers', home.ausers, name='ausers'),
    path('forgot', home.forgot, name="forgot"),
    path('forgotpassword', home.forgotpassword, name="forgotpassword"),
    url('vgp', home.vgp, name='vgp'),
    path('gpvst', home.gpvst, name='gpvst'),
]

urlpatterns+=staticfiles_urlpatterns(

)