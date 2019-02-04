import csv
import shutil
from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
import os
import subprocess
import datetime
from django.conf import settings
from django.contrib.sessions.models import Session
from django.template import RequestContext
from letscode.models import users
from django.contrib import messages
from django.core.mail import send_mail

un=""
def my(request):
    return render(request,'homepage.html',{})

def log(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c1 = con.cursor()
    c1.execute('use msit')
    s1=""
    s2=""
    u=""
    p=""
    if request.method=='POST':
        u=request.POST.get('uemail')
        p=request.POST.get('upwd')

    s="select urole,uid from letscode_users where uemail = "+"'"+u+"' and pwd= "+"'"+p+"'"
    c1.execute(s)

    for row in c1:
        #print(row)
        s1=row[0]
        s2=row[1]
        #print(s2,"     R  A   J    U")

        #print(s1,"    ",s2)
    #print(cur.rowcount)
    if c1.rowcount==0 or c1.rowcount==-1:
        return render(request,'homepage.html',{'y':'user doesn\'t exist'})
    else:
        if(s1=='admin'):
            request.session['id'] = s2
            return render(request,'admin_home.html',{})
        elif(s1=='student'):
            request.session['id'] = s2
            return render(request,'student_home.html',{})
        else:
            request.session['id'] = s2
            return render(request,'mentor_home.html',{})


def questIn(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cur = con.cursor()
    cur.execute('use msit')
    s1=""
    ff1=""
    ff2=""
    ff3=""
    ff4=""
    ff5=""
    ff6=""
    cs=""
    input=[]
    output=[]
    pt=""
    if request.method=="POST":
        ff1=request.POST.get('qid')
        ff2=request.POST.get('qname')
        ff3=request.POST.get('qtext')
        ff4=request.POST.get('file')
        ff5=request.POST.get('tester')
        ff6=request.POST.get('code')
        if ff1!="" and ff2!="" and ff3!="" and ff4!="" and ff5!="" and ff6!="":
            #print(ff1,' ',ff2,' ',ff3,' ',ff4,' ',ff5,' ',ff6,'    ------------------')
            w1=ff1[:1].upper()
            cs=w1+ff1[1:]
            #print(cs,"   ---------------")
            #cwd = os.getcwd()
            #path2=cwd+"\\javaprograms\\"+cs+".java"
            #print(cwd," *************")
            #with open(path2,"w") as f:
                #f.write(ff5)
            pt=os.path.abspath(ff4)
            #print(pt," @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            try:
                cur.execute("INSERT questions VALUES(%s,%s,%s,%s,%s)", (ff1,ff2,ff3,ff5,ff6))
                con.commit()
            except:
                return render(request,'mentor_create_question.html', {'msg':"qid has already existed ! please try again"})

            with open(pt) as f:
                gf=0
                for g in f:
                    if g.strip()=="break":
                        gf=1
                    if gf==0:
                        input.append(g.strip())
                    elif gf==1 and g.strip()!="break":
                        output.append(g.strip())


            for h1,h2 in zip(input,output):
                #print(h1+"  "+h2)
                cur.execute("INSERT testcases VALUES(%s,%s,%s)", (ff1,h1,h2))
                con.commit()

            return render(request, 'mentor_create_question.html', {'msg':"question is created sucessfully"})

        else:
            return render(request, 'mentor_create_question.html', {'msg':"please fill all the fields"})

def mtest(request):
    return render(request,"mentor_create_question.html",{})

def mhome(request):
    return render(request, 'mentor_home.html', {'y': un})

def viewQuestions(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c2 = con.cursor()
    c2.execute('use msit')
    res="select * from questions"
    c2.execute(res)
    my=[]
    lod=[]
    li=c2.fetchall()
    for k in li:
        jk=[]
        #print(k[0],"  ////////////////////////////")
        jk.append(k)
        res2="select qin,qout from testcases where qid='"+k[0]+"'"
        c2.execute(res2)
        km=c2.fetchall()
        for ha in km:
            #print(ha)
            jk.append(ha)
        my.append(jk)
    kl=0
    for gk in my:
        i = 0
        for hk in gk:
            if i==0:
                if kl==0:
                    for yk in hk:
                        #print(yk)
                        lod.append(yk)
                    kl=1
                else:
                    #print("break (((((((((((((((((((((((((((((((")
                    lod.append("break")
                    for yk in hk:
                        #print(yk)
                        lod.append(yk)
                #print("test cases  -----------------------------")
                lod.append("test cases")
                i=1
            else:

                for nk in hk:
                    #print(nk)
                    lod.append(nk)
                #print(hk," &&&&&&&&&&&&&&&&&&&&&&&&&")

    #for sm in lod:
        #print(sm)
        #print(gk,"  -------------------------------")

    return render(request,'mentor_view_questions.html',{'lt':lod})

def ctext(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c = con.cursor()
    c.execute('use msit')
    u=[]
    vv=[]
    s="select qid,qtest from questions"
    c.execute(s)
    ld=c.fetchall()

    for hb in ld:
        #print(hb," ************************")
        st=""
        i=0
        for ds in hb:
            if i==0:
                #print(ds ,'      -----------------------')
                st=st+ds+" ---- "
                i=1
            else:
                st=st+ds
        u.append(st)

    #for km in u:
        #for nj in km:
            #print(nj,"  ******")

    return render(request,'mentor_create_test.html',{'ad':u})


def testin(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c3 = con.cursor()
    c3.execute('use msit')
    t1=""
    t2=""
    t3=""
    t4=""
    if request.method == "POST":
        t1 = request.POST.get('tid')
        t2 = request.POST.get('qid')
        t3 = request.POST.get('active')
        t4 = request.POST.get('ms')

    #print(t1,"  ",t2," ",t3," ----------------------")
    if t1!="" and t2!="" and t3!="" and t4!="":
        no = t2.find(" ")
        # print( no,"  &&&&&&&&&&&&&&&")
        t2 = t2[0:2]
        # print(t2,"      ----------------")
        # return render(request,"mentor_create_test.html",{})
        c3.execute("INSERT  tests(tname,qid,active,max_score) VALUES(%s,%s,%s,%s)", (t1, t2, t3,int(t4)))
        con.commit()
        return render(request,'mentor_create_test.html',{'msg':"successfully inserted"})
    else:
        return render(request, 'mentor_create_test.html', {'msg': "please fill all feilds"})

def viewTests(request):
    #print("-----------       HELLO     -------------------------")
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c4 = con.cursor()
    c5=con.cursor()
    c6=con.cursor()
    c4.execute('use msit')
    kk=[]
    kk.append("Test Id")
    kk.append("Test Name")
    kk.append("Active")
    kk.append("Max Score")
    kk.append("Question Id")
    kk.append("Question Name")
    kk.append("Question Test")
    kk.append("Tester")
    kk.append("User code")
    w="select * from tests"
    c4.execute(w)
    hf=[]
    df=c4.fetchall()

    for af in df:
        i=0
        j=0
        #print(af[2])
        se=af[2]
        #print(se,"                ###################################")
        for vf in af:
            if vf!=se:
                #print(vf,"  -------------------")
                if i==0 or i==3:
                    #print(kk[i]+" : "+str(vf),"  **********************   ")
                    hf.append(kk[i]+" : "+str(vf))
                else:
                    #print(kk[i]+" : "+vf," ----------------------")
                    hf.append(kk[i]+" : "+vf)
                i=i+1
        qw="select * from questions where qid='"+se+"'"
        c5.execute(qw)
        ef=c5.fetchall()
        for yf in ef:
            for lf in yf:
                #print(kk[i]+" : "+lf,"  ------------------")
                hf.append(kk[i]+" : "+lf)
                i=i+1
        #print(se)
        rf="select * from testcases where qid='"+se+"'"
        c6.execute(rf)
        xf=c6.fetchall()
        #print("Test Cases : "+"test cases",' -------------------------')
        hf.append("Test Cases")
        for zf in xf:
            for iy in zf:
                if iy!=se:
                    #print(iy)
                    hf.append(iy)
        hf.append("break")

    #for my in hf:
        #print(my, "      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    return render(request,"mentor_view_tests.html",{'sa':hf[0:-1]},{'nh':kk})

def logout(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c7 = con.cursor()
    c7.execute('use msit')
    sk = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    #print(sk)
    c7.execute("delete from django_session where session_key='"+sk+"'")
    #print("-----------------------")
    con.commit()
    #print(ew,"  ******************************************")
    return render(request,"homepage.html",{})

def shome(request):
    return render(request,"student_home.html",{})

def satest(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c7 = con.cursor()
    c7.execute('use msit')
    aws="select qid from tests where active='true'"
    c7.execute(aws)
    lq=c7.fetchall()
    ka=[]
    for uu in lq:
        #print(uu, "   ---------------------------")
        for yg in uu:
            #print(yg+"     ")
            ww="select qname from questions where qid='"+yg+"'"
            c7.execute(ww)
            dc=c7.fetchall()
            for hm in dc:
                for jb in hm:
                    #print(jb,"  ------------------",yg)
                    ka.append(yg+"-"+jb)
        #print("    BREAK  ")
    le = len(ka)
    #print(le," **************************************************************************")
    return render(request,"student_available_tests.html",{'ma':ka,'ra':le})

def takeTest(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    c8 = con.cursor()
    c8.execute('use msit')
    ju=""
    sg=""
    st=""
    yv=""
    vk=""
    dn=""
    jr=""
    if request.method == 'POST':
        u = request.POST.get('test')
        ju=str(u)
    #print(u," *****************")
    #print(ju," ----------------------")
    if ju!="None":

        oi=ju.find("-")
        #print(oi," ------------------------------------------")
        ju=ju[0:oi]
        #print(ju,"    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        vak="select qtest,qcode from questions where qid='"+ju+"'"
        c8.execute(vak)
        hr=c8.fetchall()
        r=0
        for lk in hr:
            for vs in lk:
                if r==0:
                    #print(vs)
                    i1 = vs.find('sample input')
                    i2 = i1 + 12
                    i3 = vs.find('sample output')
                    i4 = i3 + 13
                    sg=vs[0:i1].strip()
                    st=vs[i1:i2].strip()
                    yv=vs[i2:i3].strip()
                    vk=vs[i3:i4].strip()
                    dn=vs[i4:].strip()
                    r=1
                else:
                    jr=vs
                    r=0

        #print("---------------------------------------------")
        #print(sg).
        #print(st)
        #print(yv)
        #print(vk)
        #print(dn)
        #print("---------------------------------------------")
        return render(request,'student_take_test.html',{'sp1':sg,'sp2':st,'sp3':yv,'sp4':vk,'sp5':dn,'sp6':jr,'id':ju})
    else:
        #print(" - ------- ---- -----")
        con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
        c7 = con.cursor()
        c7.execute('use msit')
        aws = "select qid from tests where active='true'"
        c7.execute(aws)
        lq = c7.fetchall()
        ka = []
        for uu in lq:
            # print(uu, "   ---------------------------")
            for yg in uu:
                # print(yg+"     ")
                ww = "select qname from questions where qid='" + yg + "'"
                c7.execute(ww)
                dc = c7.fetchall()
                for hm in dc:
                    for jb in hm:
                        # print(jb,"  ------------------",yg)
                        ka.append(yg + "-" + jb)
            # print("    BREAK  ")
        le = len(ka)
        # print(le," **************************************************************************")
        return render(request, "student_available_tests.html", {'ma': ka, 'ra': le,'msg':"please select one"})



def execute(request):
    #print("**************************************************************")
    sjs=0
    tjs=0
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cc = con.cursor()
    vc = con.cursor()
    xc = con.cursor()
    cc.execute('use msit')
    mim=""
    mnm=""
    path=""
    stg=""
    mm1=""
    mm2=""
    mm3=""
    mm4=""
    mm5=""
    idi=""
    cn=""
    om=""
    cwd2=""
    pat3=""
    pat2=""
    ses=""
    ppt = os.getcwd()
    if request.method == 'POST':
        cm = request.POST.get('code')
        #print(cm," @@@@@@@@@@@@@@@@@@@@@@@@@@@")
        mim = cm
        idi=request.POST.get('id')
        stg=idi
    #print(stg,"  -----------RAJU")
    # insert into code , qid  ,uid  into coding table
    ud=request.session['id']
    #print(ud,"  ********")

    vc.execute("select * from coding where qid='"+idi+"'")
    py=vc.fetchone()
    #print(py,"   //////////////////////")
    if py==None:
        #print("---------")
        xc.execute("INSERT coding VALUES(%s,%s,%s)", (ud,idi,cm))
        con.commit()
    else:
        #print("**********")
        asa="delete from coding where qid='"+idi+"'"
        #print(asa,"  --------------------------------")
        vc.execute(asa)
        con.commit()
        xc.execute("INSERT coding VALUES(%s,%s,%s)", (ud, idi, cm))
        con.commit()


    ew="select qtest,qtester from questions where qid='"+stg+"'"
    cc.execute(ew)
    gfe=cc.fetchall()
    z=0
    for tye in gfe:
        for fet in tye:
            if z==0:
                #print(fet,"    !!!!!!!!!!!!")
                i1 = fet.find('sample input')
                i2 = i1 + 12
                i3 = fet.find('sample output')
                i4 = i3 + 13
                mm1 = fet[0:i1].strip()
                mm2 = fet[i1:i2].strip()
                mm3 = fet[i2:i3].strip()
                mm4 = fet[i3:i4].strip()
                mm5 = fet[i4:].strip()
                #print(mm1," ",mm2," ",mm3," ",mm4," ",mm5," ---------------------------------")
                z=1
            else:
                #print(type(fet),"  |||||||||||||")
                ss=fet
                nn=ss.find('class ')
                ss=ss[nn+6:]
                mm=ss.find('{')
                ss=ss[:mm-1]
                #print(ss)
                ses=str(request.session['id'])
                pp="b"+ses[:2]
                #print(pp)
                pat3=ppt+"\\"+pp+"\\"+ses+"\\"
                pat2=pat3+ss.strip()+".java"
                #print(pat2,"****")
                try:
                    with open(pat2,'w') as f:
                        f.write(fet)
                except:
                    return render(request,'student_take_test.html',{'sp1': mm1, 'sp2': mm2, 'sp3': mm3, 'sp4': mm4, 'sp5': mm5, 'sp6': mim, 'id': idi})

    z=stg[:1].upper()
    om=z+stg[1:]
    #print(z,"    !!!!!!!!!!!!!!!!!!!!")
    cn=z+stg[1:]+".java"
    path3=pat3+cn
    #print(path3," +++++")

    #print(mim," ###################")
    s1 = mim.find("class ")
    #print(s1,"     @@@@@")
    s2=mim[s1+6:]
    #print(s2,"  #####")
    s3=s2.find('{')
    s4=s2[:s3]
    #print(s4,"  ###########")
    s4=s4.strip()
    #print(len(s4),"           ------")
    #print(s4," ********************")
    npt=s4+'.java'
    #print(npt,"    -----------------")
    #cwd3=os.getcwd()
    path4=pat3+npt
    #print(path4," --------")
    with open(path4, "w") as f:
        f.write(cm)


    cmd1="javac -d . "+path4
    #print(cmd1," **************")
    proc1=subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out1,err1=proc1.communicate()
    yq1 = "\\t"
    yq2 = "\\r"
    yq3 ="\\"
    zex1 = []
    for xx in err1.splitlines():
        yr = str(xx)
        if "letscode" in yr:
            km=yr.find("letscode")
            yr=yr[km+23:]

        yr = yr.replace(yq1, "")
        yr = yr.replace(yq2, "")
        yr = yr.replace(yq3, "")
        #print(yr[2:-1])
        zex1.append(yr[2:-1])

        #for tr in zex1:
           #print(tr)
    #print(len(zex1)," ---------")
    if len(zex1)==0:
        sjs=1
        #print("compilation sucessfull")

    if sjs==0:
        return render(request, 'student_take_test.html',{'sp1': mm1, 'sp2': mm2, 'sp3': mm3, 'sp4': mm4, 'sp5': mm5, 'sp6': mim, 'id': idi, 'sp': zex1})
    else:
        #print(pat2," *********")
        cmd2="javac -d . "+pat2
        proc2=subprocess.Popen(cmd2,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2,err2=proc2.communicate()
        zq1="\\t"
        zq2="\\r"
        zex2=[]
        for ds in err2.splitlines():
            ar = str(ds)
            ar = ar.replace(zq1,"")
            ar = ar.replace(zq2,"")
            zex2.append(ar[2:-1])

        #for hrm in zex2:
            #print(hrm)

        if len(zex2)==0:
            tjs=1
            #print("ssssssssssssssssssssssssssssssssssss")

        if tjs==0:
             return render(request, 'student_take_test.html',{'sp1': mm1, 'sp2': mm2, 'sp3': mm3, 'sp4': mm4, 'sp5': mm5, 'sp6': mim, 'id': idi,'sp': zex2})
        else:
            #print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$")
            zex3=[]
            #print(cmd2)
            q1 = os.popen(cmd2).read()
            kkh="java ex."+om
            #print(kkh,"   ??????")
            a = os.popen(kkh).read()
            wer=str(a)
            #print(wer)
            jk=wer.find("score is")
            #print(jk," -----")
            rk=wer[jk+9:-1]
            #print(rk," +++++++++++++++++++++++++++++++++++")
            ra=int(rk.strip())
            #print(ra,type(ra))
            dt = datetime.date.today()
            if ra==0:
                cc.execute("select * from results where uid='"+ses+"'"+" and qid ='"+idi+"'")
                od=cc.fetchone()
                #print(od, " ------------------------------------------------------------------------")
                if od==None:
                    cc.execute("INSERT results VALUES(%s,%s,%s,%s,%s)", (ses,idi,int(ra),dt,"Fail"))
                    con.commit()
                else:
                    cc.execute("delete from results where uid='"+ses+"'"+" and qid ='"+idi+"'")
                    con.commit()
                    cc.execute("INSERT results VALUES(%s,%s,%s,%s,%s)",(ses, idi, int(ra), dt, "Fail"))
                    con.commit()

            elif ra==10:
                cc.execute("select * from results where uid='"+ses+"'"+" and qid ='"+idi+"'")
                od = cc.fetchone()
                #print(od, " ------------------------------------------------------------------------")
                if od == None:
                    cc.execute("INSERT results VALUES(%s,%s,%s,%s,%s)", (ses, idi, int(ra), dt, "Pass"))
                    con.commit()
                else:
                    cc.execute("delete from results where uid='"+ses+"'"+" and qid ='"+idi+"'")
                    con.commit()
                    cc.execute("INSERT results VALUES(%s,%s,%s,%s,%s)",(ses, idi, int(ra), dt, "Pass"))
                    con.commit()

            zex3.append(wer)
            #print(wer," -------------------")
            return render(request, 'student_take_test.html',{'sp1': mm1, 'sp2': mm2, 'sp3': mm3, 'sp4': mm4, 'sp5': mm5, 'sp6': mim, 'id': idi,'sp': zex3})




def qedit(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv1 = con.cursor()
    cv1.execute('use msit')
    vb="select qid,qtest from questions"
    cv1.execute(vb)
    vb2=cv1.fetchall()
    jh=[]
    kl=0
    for fg in vb2:
        #print(fg ," ----------------- ")
        u=0
        ss=""
        for gf in fg:
            #print(gf," ---------")
            if u==0:
                ss=gf+" -- "
                u=1
            else:
                ss=ss+gf
        #print(ss,"  ------")
        jh.append(ss)
    #for bh in jh:
        #print(bh)
    kl=len(jh)
    return render(request, 'mentor_q_edit.html',{'k2':jh,'k3':kl})

def editform(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv2 = con.cursor()
    cv2.execute('use msit')
    as1=""
    as2=""
    as3=""
    as4=""
    as5=""
    if request.method == 'POST':
        cm = request.POST.get('et')
    #print(cm," ----- ")
    if cm!=None:
        ssq=cm.find(" --")
    #print(ssq)
        sq2=cm[:ssq]
    #print(sq2)
        he="select * from questions where qid='"+sq2+"'"
        cv2.execute(he)
        ws=cv2.fetchone()
        as1=str(ws[0])
        as2 = str(ws[1])
        as3 = str(ws[2])
        as4 = str(ws[3])
        as5 = str(ws[4])

        #print(as1,"   ",as2,"  ",as3,"  ",as4,"  ",as5)
        #for ac in ws:
            #print(ac)

        return render(request,'mentor_edit_question_form.html',{'t1':as1,'t2':as2,'t3':as3,'t4':as4,'t5':as5})
    else:
        con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
        cv1 = con.cursor()
        cv1.execute('use msit')
        vb = "select qid,qtest from questions"
        cv1.execute(vb)
        vb2 = cv1.fetchall()
        jh = []
        kl = 0
        for fg in vb2:
            # print(fg ," ----------------- ")
            u = 0
            ss = ""
            for gf in fg:
                # print(gf," ---------")
                if u == 0:
                    ss = gf + " -- "
                    u = 1
                else:
                    ss = ss + gf
            # print(ss,"  ------")
            jh.append(ss)
        # for bh in jh:
        # print(bh)
        kl = len(jh)
        return render(request, 'mentor_q_edit.html', {'k2': jh, 'k3': kl,'msg':"please select one "})
def qed(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv3 = con.cursor()
    cv3.execute('use msit')

    sd1=""
    sd2=""
    sd3=""
    sd4=""
    sd5=""
    sd6=""
    inp=[]
    outp=[]
    if request.method=='POST':
        sd1 = request.POST.get('qid')
        sd2 = request.POST.get('qname')
        sd3 = request.POST.get('qtext')
        sd4 = request.POST.get('file')
        sd5 = request.POST.get('tester')
        sd6 = request.POST.get('code')
    #print(sd6," -------------------------")
    if sd1!="" and sd2!="" and sd3!="" and sd4!="" and sd5!="" and sd6!="":

        w1 = sd1[:1].upper()
        cs = w1 + sd1[1:]
        # print(cs,"   ---------------")
        #cwd = os.getcwd()
        #path2 = cwd + "\\javaprograms\\" + cs + ".java"
        # print(cwd," *************")
        #with open(path2, "w") as f:
            #f.write(sd5)

        sf="delete from questions where qid='"+sd1+"'"
        cv3.execute(sf)
        cv3.execute("INSERT questions VALUES(%s,%s,%s,%s,%s)", (sd1,sd2,sd3,sd5,sd6))
        con.commit()
        pt = os.path.abspath(sd4)
        with open(pt) as f:
            gf = 0
            for g in f:
                if g.strip() == "break":
                    gf = 1
                if gf == 0:
                    inp.append(g.strip())
                elif gf == 1 and g.strip() != "break":
                    outp.append(g.strip())

        for h1, h2 in zip(inp, outp):
            #print(h1 + "  " + h2)
            cv3.execute("INSERT testcases VALUES(%s,%s,%s)", (sd1, h1, h2))
            con.commit()

        con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
        c2 = con.cursor()
        c2.execute('use msit')
        res="select * from questions"
        c2.execute(res)
        my=[]
        lod=[]
        li=c2.fetchall()
        for k in li:
            jk=[]
            #print(k[0],"  ////////////////////////////")
            jk.append(k)
            res2="select qin,qout from testcases where qid='"+k[0]+"'"
            c2.execute(res2)
            km=c2.fetchall()

            for ha in km:
                #print(ha)
                jk.append(ha)
            my.append(jk)
        kl=0
        for gk in my:
            i = 0
            for hk in gk:
                if i==0:
                    if kl==0:
                        for yk in hk:
                            #print(yk)
                            lod.append(yk)
                        kl=1
                    else:
                        #print("break (((((((((((((((((((((((((((((((")
                        lod.append("break")
                        for yk in hk:
                            #print(yk)
                            lod.append(yk)
                         #print("test cases  -----------------------------")
                    lod.append("test cases")
                    i=1
                else:

                    for nk in hk:
                        #print(nk)
                        lod.append(nk)
                    #print(hk," &&&&&&&&&&&&&&&&&&&&&&&&&")

        #for sm in lod:
            #print(sm)
            #print(gk,"  -------------------------------")

        return render(request,'mentor_view_questions.html',{'lt':lod,"msg":"question is edited successfully"})
    else:
        con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
        cv1 = con.cursor()
        cv1.execute('use msit')
        vb = "select qid,qtest from questions"
        cv1.execute(vb)
        vb2 = cv1.fetchall()
        jh = []
        kl = 0
        for fg in vb2:
            # print(fg ," ----------------- ")
            u = 0
            ss = ""
            for gf in fg:
                # print(gf," ---------")
                if u == 0:
                    ss = gf + " -- "
                    u = 1
                else:
                    ss = ss + gf
            # print(ss,"  ------")
            jh.append(ss)
        # for bh in jh:
        # print(bh)
        kl = len(jh)
        return render(request, 'mentor_q_edit.html', {'k2': jh, 'k3': kl,'msg':" didn't fill all fields !!! please try again "})

def etest(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv3 = con.cursor()
    cv3.execute('use msit')
    uf="select tid,tname from tests"
    cv3.execute(uf)
    usd=cv3.fetchall()
    jh = []
    kl = 0
    for fg in usd:
        # print(fg ," ----------------- ")
        u = 0
        ss = ""
        for gf in fg:
            # print(gf," ---------")
            if u == 0:
                ss = str(gf) + " -- "
                u = 1
            else:
                ss = ss + gf
        #print(ss,"  ------")
        jh.append(ss)
    # for bh in jh:
    # print(bh)
    kl = len(jh)
    return render(request,'mentor_t_edit.html',{'k2':jh,'k3':kl})

def teform(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv4 = con.cursor()
    cv4.execute('use msit')
    qa=""
    aq=""
    rd=""
    if request.method=='POST':
        qa=request.POST.get('et')

    if qa!=None:
        #print(qa)
        sd=qa.find(" -")
        aq=qa[:sd]
        #print(aq)
        tn=int(aq)
        tt="select * from tests where tid= %s "% int(tn)
        #print(type(tn),"  ",tn)
        cv4.execute(tt)
        rt=cv4.fetchone()
        #for gt in rt:
            #print(gt," ***** ")
        rd=rt[1]
        #print(rd,"------------------------------------")

        u = []
        vv = []
        s = "select qid,qtest from questions"
        cv4.execute(s)
        ld = cv4.fetchall()

        for hb in ld:
            # print(hb," ************************")
            st = ""
            i = 0
            for ds in hb:
                if i == 0:
                    # print(ds ,'      -----------------------')
                    st = st + ds + " ---- "
                    i = 1
                else:
                    st = st + ds
            u.append(st)

        return render(request,'mentor_edit_test_form.html',{"cv":rd,'ad':u,"id":aq})
    else:
        return render(request,'mentor_t_edit.html',{'msg':"please select one"})

def qdel(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv1 = con.cursor()
    cv1.execute('use msit')
    vb="select qid,qtest from questions"
    cv1.execute(vb)
    vb2=cv1.fetchall()
    jh=[]
    kl=0
    for fg in vb2:
        #print(fg ," ----------------- ")
        u=0
        ss=""
        for gf in fg:
            #print(gf," ---------")
            if u==0:
                ss=gf+" -- "
                u=1
            else:
                ss=ss+gf
        #print(ss,"  ------")
        jh.append(ss)
    #for bh in jh:
        #print(bh)
    kl=len(jh)
    return render(request, 'mentor_q_del.html', {'k2': jh, 'k3': kl})
def questdel(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv4 = con.cursor()
    cv4.execute('use msit')
    val=""
    if request.method=='POST':
        val=request.POST.get('dt')
    if val!="":
        #print(val)
        oo=val.find(" -")
        val2=val[:oo]
        #print(val2+"&&&&&")
        xr="delete from questions where qid='"+val2+"'"
        cv4.execute(xr)
        con.commit()

        con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
        c2 = con.cursor()
        c2.execute('use msit')
        res = "select * from questions"
        c2.execute(res)
        my = []
        lod = []
        li = c2.fetchall()
        for k in li:
            jk = []
            # print(k[0],"  ////////////////////////////")
            jk.append(k)
            res2 = "select qin,qout from testcases where qid='" + k[0] + "'"
            c2.execute(res2)
            km = c2.fetchall()
            for ha in km:
                # print(ha)
                jk.append(ha)
            my.append(jk)
        kl = 0
        for gk in my:
            i = 0
            for hk in gk:
                if i == 0:
                    if kl == 0:
                        for yk in hk:
                            # print(yk)
                            lod.append(yk)
                        kl = 1
                    else:
                        #print("break (((((((((((((((((((((((((((((((")
                        lod.append("break")
                        for yk in hk:
                            # print(yk)
                            lod.append(yk)
                    # print("test cases  -----------------------------")
                    lod.append("test cases")
                    i = 1
                else:

                    for nk in hk:
                        # print(nk)
                        lod.append(nk)
                    # print(hk," &&&&&&&&&&&&&&&&&&&&&&&&&")

        # for sm in lod:
        # print(sm)
        # print(gk,"  -------------------------------")

        return render(request, 'mentor_view_questions.html', {'lt': lod,'msg':"question is deleted successfully"})
    else:
        return render(request,'mentor_q_del.html',{'msg':"please select one "})

def tediting(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cd2 = con.cursor()
    cd2.execute('use msit')
    tu0=""
    tu1=""
    tu2=""
    tu3=""
    tu4=""
    ry=0
    oi=""
    if request.method=='POST':
        ty0=request.POST.get('tid')
        ty1=request.POST.get('tname')
        ty2=request.POST.get('qid')
        ty3= request.POST.get('active')
        ty4 = request.POST.get('ms')
        tu0=ty0
        tu1=ty1
        tu2=ty2
        tu3=ty3
        tu4=ty4
        ry=int(ty0)
    #print(tu0," ",tu1," ",tu2," ",tu3," ",tu4)
    fd=tu2.find(" -")
    oi=tu2[:fd]
    #print(oi)

    if tu1!="" and tu2!="" and tu3!="" and  tu4!="":
       bh="delete from tests where tid=%s"% int(ry)
       cd2.execute(bh)
       cd2.execute("INSERT tests VALUES(%s,%s,%s,%s,%s)",(int(ry),tu1,oi,tu3,int(tu4)))
       con.commit()

       # print("-----------       HELLO     -------------------------")
       con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
       c4 = con.cursor()
       c5 = con.cursor()
       c6 = con.cursor()
       c4.execute('use msit')
       kk = []
       kk.append("Test Id")
       kk.append("Test Name")
       kk.append("Active")
       kk.append("Max Score")
       kk.append("Question Id")
       kk.append("Question Name")
       kk.append("Question Test")
       kk.append("Tester")
       kk.append("User code")
       w = "select * from tests"
       c4.execute(w)
       hf = []
       df = c4.fetchall()

       for af in df:
           i = 0
           j = 0
           # print(af[2])
           se = af[2]
           # print(se,"                ###################################")
           for vf in af:
               if vf != se:
                   # print(vf,"  -------------------")
                   if i == 0 or i == 3:
                       # print(kk[i]+" : "+str(vf),"  **********************   ")
                       hf.append(kk[i] + " : " + str(vf))
                   else:
                       # print(kk[i]+" : "+vf," ----------------------")
                       hf.append(kk[i] + " : " + vf)
                   i = i + 1
           qw = "select * from questions where qid='" + se + "'"
           c5.execute(qw)
           ef = c5.fetchall()
           for yf in ef:
               for lf in yf:
                   #print(kk[i] + " : " + lf, "  ------------------")
                   hf.append(kk[i] + " : " + lf)
                   i = i + 1
           # print(se)
           rf = "select * from testcases where qid='" + se + "'"
           c6.execute(rf)
           xf = c6.fetchall()
           hf.append("Test Cases")
           for zf in xf:
               for iy in zf:
                   if iy != se:
                       # print(iy)
                       hf.append(iy)
           hf.append("break")

       return render(request, "mentor_view_tests.html", {'sa':hf[0:-1],'nh':kk,'msg':"test is edited successfully"})

    else:
        return render(request,"mentor_t_edit.html",{"msg":"didn't fill all fields !!! please try again"})

def tdel(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv3 = con.cursor()
    cv3.execute('use msit')
    uf = "select tid,tname from tests"
    cv3.execute(uf)
    usd = cv3.fetchall()
    jh = []
    kl = 0
    for fg in usd:
        # print(fg ," ----------------- ")
        u = 0
        ss = ""
        for gf in fg:
            # print(gf," ---------")
            if u == 0:
                ss = str(gf) + " -- "
                u = 1
            else:
                ss = ss + gf
        #print(ss, "  ------")
        jh.append(ss)
    kl = len(jh)
    return render(request, 'mentor_t_del.html', {'k2': jh, 'k3': kl})

def tdl(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv8 = con.cursor()
    cv8.execute('use msit')

    pq=""
    vc=""
    vc2=0
    if request.method=='POST':
        bq=request.POST.get('dt')
        pq=bq
    if pq!="":
        hb=pq.find(" -")
        vc=pq[:hb]
        vc2=int(vc)
        #print(type(vc2)," ",vc2)
        bus = "delete from tests where tid=%s"%int(vc2)
        cv8.execute(bus)
        con.commit()

        con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
        c4 = con.cursor()
        c5 = con.cursor()
        c6 = con.cursor()
        c4.execute('use msit')
        kk = []
        kk.append("Test Id")
        kk.append("Test Name")
        kk.append("Active")
        kk.append("Max Score")
        kk.append("Question Id")
        kk.append("Question Name")
        kk.append("Question Test")
        kk.append("Tester")
        kk.append("User code")
        w = "select * from tests"
        c4.execute(w)
        hf = []
        df = c4.fetchall()

        for af in df:
            i = 0
            j = 0
            # print(af[2])
            se = af[2]
            # print(se,"                ###################################")
            for vf in af:
                if vf != se:
                    # print(vf,"  -------------------")
                    if i == 0 or i == 3:
                        # print(kk[i]+" : "+str(vf),"  **********************   ")
                        hf.append(kk[i] + " : " + str(vf))
                    else:
                        # print(kk[i]+" : "+vf," ----------------------")
                        hf.append(kk[i] + " : " + vf)
                    i = i + 1
            qw = "select * from questions where qid='" + se + "'"
            c5.execute(qw)
            ef = c5.fetchall()
            for yf in ef:
                for lf in yf:
                    #print(kk[i] + " : " + lf, "  ------------------")
                    hf.append(kk[i] + " : " + lf)
                    i = i + 1
            # print(se)
            rf = "select * from testcases where qid='" + se + "'"
            c6.execute(rf)
            xf = c6.fetchall()
            # print("Test Cases : "+"test cases",' -------------------------')
            hf.append("Test Cases")
            for zf in xf:
                for iy in zf:
                    if iy != se:
                        # print(iy)
                        hf.append(iy)
            hf.append("break")

        return render(request, "mentor_view_tests.html", {'sa':hf[0:-1],'nh': kk,'msg':"test is deleted successfully"})
    else:
        return render(request,'mentor_t_del.html',{'msg':"please select one"})


def adminhome(request):
    return render(request,'admin_home.html',{})

def upload(request):
   return render(request,"addusers.html",{})

def list(request):
    #print("method calling")
    posts=users.objects.all()
    #print(posts,"   ------------------------")
    return render(request,"users_view.html",{'posts':posts})

def dataupload(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cv9 = con.cursor()
    cv9.execute('use msit')
    jp=""
    bn=""
    f1=""
    bpt=""
    if request.method=='POST':
        bname=request.POST.get('batch')
        file1=request.POST.get('upload')
        bn=bname
        hd=bn[1:3]
        f1=file1
        if bn!="" and f1!="":
            #print(type(file1)," /////////")
            pat=os.getcwd()
            jp=pat+"\\"+f1
            #print(jp," -----")
            #print(type(bname)," ")
            bpt=pat+"\\"+bn+"\\"
            if not os.path.exists(bn):
                os.makedirs(bn)
            else:
                return render(request,'addusers.html',{"msg":"batch name is already existed"})
            with open(jp) as ap:
                vip=csv.reader(ap,delimiter=',')
                #print(vip)
                for dp in vip:
                    if dp[2][:2]==hd:
                        print(dp[2],"              -----------------------------")
                        if not os.path.exists(bpt+dp[2]):
                            os.makedirs(bpt+dp[2])
                        try:
                            cv9.execute("INSERT letscode_users VALUES(%s,%s,%s,%s,%s,%s,%s)", (dp[0],dp[1],dp[2],dp[3],dp[4],dp[5],dp[6]))
                            con.commit()
                            cv9.execute("INSERT into all_users VALUES ('"+dp[2]+"')")
                            con.commit()
                        except:
                            #print("*****************************************")
                            return render(request,'addusers.html',{'msg':"batch is already updated"})
                cv9.execute("INSERT into batch VALUES ('"+bn+"')")
                con.commit()
            return render(request,'addusers.html',{'msg':"File is uploaded successfully"})
        else:
            return render(request,'addusers.html',{'msg':"please fill all details"})

def results(request):
    yi=""
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    cd = con.cursor()
    cd.execute('use msit')
    idi=request.session['id']
    pj="select * from results where uid='"+idi+"'"
    cd.execute(pj)
    maa=[]
    vu=cd.fetchall()
    for gg in vu:
        #print(gg, " ------")
        yi=gg[1]
        #print(yi)
        fs=""
        cd.execute("select qtest from questions where qid='"+yi+"'")
        tr=cd.fetchone()
        for iy in tr:
            #print(iy)
            fs=iy
        maa.append(gg[0])
        maa.append(gg[1])
        maa.append(fs)
        maa.append(gg[2])
        maa.append(gg[3])
        maa.append(gg[4])
        #print(maa,"   ///////////")
        maa.append("break")
        #print(a,"        ******")
        #print("break  --------")
    return render(request,"results.html",{'rs':maa[:-1]})

def sres(request):
    con=mysql.connector.connect(host='localhost',user='root',password='root',db='msit')
    rc=con.cursor()
    rc.execute('use msit')
    mt=request.session['id']
    #print(mt," ----------------------")
    rc.execute("select sid from team where mid='" + mt + "'")
    nr = rc.fetchall()
    pl=[]
    for fp in nr:
        #print(fp)
        for bn in fp:
            #print(bn)
            pl.append(bn)
    vs=len(pl)
    return render(request,'mentor_student_results.html',{'rj':pl,'k3':vs})

def srt(request):
    con=mysql.connector.connect(host='localhost',user='root',password='root',db='msit')
    mc=con.cursor()
    mc.execute('use msit')
    cc=""
    if request.method=='POST':
        cc=request.POST.get('id')
    #print(cc)
    sri="select * from results where uid='"+cc+"'"
    mc.execute(sri)
    pyth=mc.fetchall()
    en=[]
    bbc=""
    for myth  in pyth:
        #print(myth)
        bbc=myth[1]
        fs = ""
        mc.execute("select qtest from questions where qid='" + bbc + "'")
        tr = mc.fetchone()
        for iy in tr:
            # print(iy)
            fs = iy

        en.append(myth[0])
        en.append(myth[1])
        en.append(fs)
        en.append(myth[2])
        en.append(myth[3])
        en.append(myth[4])
        en.append("break")
        #print("break")
    return render(request,'mentor_view_results.html',{'oi':en[:-1],'hu':cc})

def bdelete(request):
    return render(request,'admin_delete_batch.html',{})

def delbat(request):
    user="root"
    password="root"
    db="msit"
    pth=""
    con=mysql.connector.connect(host='localhost',user='root',password='root',db='msit')
    pc=con.cursor()
    vq=""
    ct=""
    pc.execute('use msit')
    if request.method=='POST':
        vq=request.POST.get('val')
        ct=request.POST.get('path')
    #print(vq)
    if vq!=None:
        if vq=="Explore Batch Details":
            if ct!="":
                pc.execute("select bname from batch")
                nu=pc.fetchone()
                if nu!=None:
                    te=""
                    for ju in nu:
                        te=ju
                    #print(ct,"   ",ct[-1:])
                    if ct[-1:]=="\\":
                        pth=ct+te+".sql"
                    else:
                        pth=ct+"\\"+te+".sql"
                    os.popen("mysqldump -u %s -p%s  %s > %s " % (user, password, db, pth))
                #print("123")
                    return render(request,'admin_delete_batch.html',{'msg':"Explore successfully"})
                else:
                    return render(request,'admin_delete_batch.html',{'msg':"There is no users database"})
            else:
                return render(request,'admin_delete_batch.html',{'msg':"please enter path"})
        elif vq=="Delete Batch Folder":
            pc.execute("select bname from batch")
            nu = pc.fetchone()
            if nu!=None:
                te = ""
                for ju in nu:
                    te = ju
                print(te," --------")
                yt=os.getcwd()
                dpath=yt+"\\"+te
                #print(yt ,"  ",te)
                try:
                    shutil.rmtree(dpath)
                    pc.execute("delete * from batch")
                except:
                    print("************************************")
                    return render(request,'admin_delete_batch.html',{'msg':"Folder doesn't exist"})
                return render(request, 'admin_delete_batch.html', {'msg': "batch folder is deleted successfully"})
            else:
                print('**********************')
                return render(request,'admin_delete_batch.html',{'msg':"there is no folder"})

        elif vq=="Delete Batch Database":
            pc.execute("delete from letscode_users where urole!='admin'")
            con.commit()
        return render(request,'admin_delete_batch.html',{'msg':"Batch is deleted from database"})
    else:
        return render(request,'admin_delete_batch.html',{'msg':"please select one"})

def updres(request):
    #print("------------------------------------------")
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    mc = con.cursor()
    mc.execute('use msit')
    cc = ""
    if request.method == 'POST':
        cc = request.POST.get('id')

    #print(cc)
    sri = "select * from coding where uid='" + cc + "'"
    mc.execute(sri)
    pyth = mc.fetchall()
    en = []
    bbc = ""
    for myth in pyth:
        #print(myth,' ')
        srmt=""
        en.append(myth[0])
        en.append(myth[1])
        srmt=str(myth[2])
        #print(srmt," ",type(srmt))
        gms=srmt.splitlines()
        for di in gms:
            #print(di," **********")
            en.append(di)
        #en.append(myth[2])
        en.append("break")
    #print(en)

    return render(request,'mentor_update_results.html',{'oi':en[:-1],'hu':cc})



def groups(request):
    con=mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    ch=con.cursor()
    ch.execute('use msit')
    fd=[]
    ch.execute("select gname from grouping")
    tt=ch.fetchall()
    #print(tt,"      ",type(tt))
    #print(len(tt))
    if len(tt)!=0:
        #print("-------------")
        for gf in tt:
            #print(gf)
            for jh in gf:
                fd.append(jh)
        rh=len(fd)
        return render(request,'admin_groups.html',{'se':fd,'k3':rh})
    else:
        #print("**************")
        return render(request,'admin_groups.html',{})

def cgp(request):
    con=mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    ch=con.cursor()
    ch.execute('use msit')
    vv=""
    vv2=""
    vv3=""
    vv4=""
    if request.method=='POST':
        vv = request.POST.get('cg')
        vv2 = request.POST.get('dg')
        vv3 = request.POST.get('au')
        vv4 = request.POST.get('grp')
    #print(vv,"  ",type(vv),"   ",vv2,"   ",type(vv2),"  ",type(vv3),"  ",vv3)
    if vv!=None:
        #print("++++++++++++++++++++++++++")
        ch.execute("select uid from letscode_users where urole='mentor'")
        ds=ch.fetchall()
        hg=[]
        for op in ds:
            #print(op)
            for yu in op:
                #print(yu)
                hg.append(yu)
        hd=len(hg)
        return render(request,'admin_create_group.html',{'k3':hd,'k2':hg})
    if vv2!=None:
        if vv4!=None:
            print(vv4)
            ch.execute("select sid from mentor_users where gname='"+vv4+"'")
            ki=ch.fetchall()
            for hg in ki:
                #print(hg)
                for sh in hg:
                    print(sh)
                    ch.execute("INSERT into all_users VALUES ('"+sh+"')")
                    con.commit()
            ch.execute("delete from mentor_users where gname='"+vv4+"'")
            con.commit()
            ch.execute("delete from grouping where gname='"+vv4+"'")
            con.commit()
            ch.execute("select * from grouping")
            jf=ch.fetchall()
            hd=[]
            for sj in jf:
                #print(sj)
                for jd in sj:
                    #print(sj)
                    hd.append(jd)
            gh=len(hd)
            return render(request, 'admin_groups.html', {'se':hd,'k3':gh})
        else:
            return render(request,'admin_groups.html',{'msg':"please select one"})


    if vv3!=None:
        #print("--------------------------")
        if vv4!=None:
            qt=[]
            ch.execute("select sid from all_users")
            tu=ch.fetchall()
            for gt in tu:
                #print(gt)
                for st in gt:
                    #print(st)
                    qt.append(st)

            mt = []
            ch.execute("select sid from mentor_users where gname='" + vv4 + "'")
            ou = ch.fetchall()
            for gt in ou:
                #print(gt)
                for st in gt:
                    #print(st)
                    mt.append(st)

            return render(request,'admin_group_users.html',{'group':vv4,'asp':qt,'users':mt})
            #print(vv4)
        else:
            return render(request, 'admin_groups.html', {'msg':"please select one "})

def cregroup(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    ch = con.cursor()
    ch.execute('use msit')
    ac=""
    bc=""
    if request.method=='POST':
        ac=request.POST.get('gn')
    if ac!="":
        try:
            ch.execute("INSERT into grouping VALUES ('"+ac+"')")
            con.commit()
        except:
            return render(request,'admin_create_group.html',{'msg':"group is already created"})
        fd = []
        ch.execute("select gname from grouping")
        tt = ch.fetchall()
        if len(tt) != 0:
            # print("-------------")
            for gf in tt:
                #print(gf)
                for jh in gf:
                    #print(jh)
                    fd.append(jh)
            rh=len(fd)
            return render(request, 'admin_groups.html', {'se': fd,'k3':rh})
        else:
            # print("**************")
            return render(request, 'admin_groups.html', {})
    else:
        #print("Ppppppppppppppppp")
        return render(request,'admin_create_group.html',{'msg':"please fill all fields"})

def ausers(request):
    b1=""
    b2=""
    b3=""
    t1=[]
    t2=[]
    tt2=[]
    gn=""
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    ch = con.cursor()
    ch.execute('use msit')
    if request.method =='POST':
        b1 = request.POST.get('add')
        b2 = request.POST.get('remove')
        b3 = request.POST.get('ctg')
        t1 = request.POST.getlist('gusers')
        t2 = request.POST.getlist('allusers')
        gn = request.POST.get('gnm')
    if b1!=None:
        if t2!=None:
            #print(t2," ------------")
            for es in t2:
                #print(es)
                ch.execute("insert mentor_users values(%s,%s)",(gn,es))
                con.commit()
                tt2.append(es)
            qt = []
            ch.execute("select sid from mentor_users where gname='"+gn+"'")
            tu = ch.fetchall()
            for gt in tu:
                # print(gt)
                for st in gt:
                    #print(st)
                    qt.append(st)

            for a in tt2:
                for b in qt:
                    if a==b:
                        #print("yes")
                        #print(b," **********************************************")
                        ch.execute("delete from all_users where sid='"+b+"'")
                        con.commit()
            ch.execute("select sid from all_users")
            bv=ch.fetchall()
            mm=[]
            for kt in bv:
                #print(kt)
                for pt in kt:
                    mm.append(pt)
            return render(request,'admin_group_users.html',{'group':gn,'users':qt,'asp':mm})
        else:
            #print(b1)
            qt = []
            ch.execute("select sid from all_users")
            tu = ch.fetchall()
            for gt in tu:
                # print(gt)
                for st in gt:
                    # print(st)
                    qt.append(st)
            return render(request,'admin_group_users.html',{'asp':qt,'group':gn,'msg':"please select atleast one student"})
    if b2!=None:
        #print(b2)
        if len(t1)!=0:
            for cr in t1:
                #print(cr," -----")
                #print(du,"  --------")
                ch.execute("delete from mentor_users where sid='"+cr+"'")
                con.commit()
                ch.execute("INSERT into all_users VALUES ('"+cr+"')")
                con.commit()

            st1 = []
            ch.execute("select sid from mentor_users where gname='"+gn+"'")
            kl = ch.fetchall()
            for bg in kl:
                #print(bg)
                for ci in bg:
                    st1.append(ci)

            st2 = []
            ch.execute("select sid from all_users")
            jl = ch.fetchall()
            for pg in jl:
                #print(pg)
                for wh in pg:
                    st2.append(wh)

            return render(request,'admin_group_users.html',{'users':st1,'asp':st2,'group':gn})
        else:
            st1 = []
            ch.execute("select sid from mentor_users where gname='"+gn+"'")
            kl = ch.fetchall()
            for bg in kl:
                #print(bg)
                for ci in bg:
                    st1.append(ci)

            st2 = []
            ch.execute("select sid from all_users")
            jl = ch.fetchall()
            for pg in jl:
                #print(pg)
                for wh in pg:
                    st2.append(wh)
            return render(request,'admin_group_users.html',{'msg':"please select atleast one student",'users':st1,'asp':st2,'group':gn})

    if b3!=None:
        ch.execute("select * from mentor_users where gname='"+gn+"'")
        ru=ch.fetchall()
        if len(ru)!=0:
            ch.execute("select * from team")
            op = ch.fetchall()
            print(op, ' ', len(op))
            if len(op)!=0:
                ch.execute("delete from team where mid='"+gn+"'")
                con.commit()
                for ug in ru:
                    #print(ug)
                    print(ug[0],"  ",ug[1])
                    ch.execute("insert team values(%s,%s)",(ug[0],ug[1]))
                    con.commit()
            else:
                for ug in ru:
                    #print(ug)
                    print(ug[0],"  ",ug[1])
                    ch.execute("insert team values(%s,%s)",(ug[0],ug[1]))
                    con.commit()


            fd = []
            ch.execute("select gname from grouping")
            tt = ch.fetchall()
            # print(tt,"      ",type(tt))
            # print(len(tt))
            if len(tt) != 0:
                # print("-------------")
                for gf in tt:
                    # print(gf)
                    for jh in gf:
                        fd.append(jh)
                rh = len(fd)

            return render(request,'admin_groups.html',{'msg':"students are added into a group successfully",'se':fd,'k3':rh})
        else:
            st1 = []
            ch.execute("select sid from mentor_users where gname='"+gn+"'")
            kl = ch.fetchall()
            for bg in kl:
                #print(bg)
                for ci in bg:
                    st1.append(ci)

            st2 = []
            ch.execute("select sid from all_users where gname='"+gn+"'")
            jl = ch.fetchall()
            for pg in jl:
                #print(pg)
                for wh in pg:
                    st2.append(wh)
            return render(request,'admin_group_users.html',{'msg':"please add atleast one student",'users':st1,'asp':st2,'group':gn})

def vgp(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    ch = con.cursor()
    ch.execute('use msit')
    ch.execute("select * from grouping")
    ar=ch.fetchall()
    dj=[]
    for ok in ar:
        #print(ok)
        for pk in ok:
            #print(pk)
            dj.append(pk)
    fy=len(dj)
    return render(request,'admin_group_view.html',{'k3':fy,'k2':dj})

def gpvst(request):
    con = mysql.connector.connect(host='localhost', user='root', password='root', db='msit')
    ch = con.cursor()
    ch.execute('use msit')
    ht=""
    oak=[]
    if request.method=='POST':
        ht=request.POST.get('gp')
    if ht!=None:
        print(ht," ----------")
        ch.execute("select sid from team where mid='"+ht+"'")
        nr=ch.fetchall()
        for ak in nr:
            #print(ak)
            for ck in ak:
                #print(ck,"**************")
                ch.execute("select * from letscode_users where uid='"+ck+"'")
                dg=ch.fetchall()
                for sg in dg:
                    #print(sg)
                    oak.append(sg[0])
                    oak.append(sg[2])
                    oak.append(sg[3])
                    oak.append(sg[4])
                    oak.append(sg[5])
                    oak.append(sg[6])
                #print("bresk"," ------------------------")
                oak.append("break")

        return render(request,'admin_view_group_students.html',{'oi':oak[:-1]})
    else:
        ch.execute("select * from grouping")
        ar = ch.fetchall()
        dj = []
        for ok in ar:
            # print(ok)
            for pk in ok:
                # print(pk)
                dj.append(pk)
        fy = len(dj)
        return render(request,'admin_group_view.html',{'msg':"please select one",'k3':fy,'k2':dj})





def forgotpassword(request):
    return render(request,"forgotpassword.html",{})


def forgot(request):
    if request.method == 'POST':
        u = request.POST.get('username', default=None)

# error = 'Invalid credentials'
    conn = mysql.connector.connect(host="localhost", user="root", password="root", db="msit")
    cursor = conn.cursor()

    cursor.execute("select uemail,pwd from letscode_users where uemail = '" + u + "'")

    for row in cursor:
        if row[0] == u:
            subject='Your password is '
            from_email = settings.EMAIL_HOST_USER
            to_list = [u, settings.EMAIL_HOST_USER]
            message=row[1]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            n="Password sent to your email"
            return render(request,"forgotpassword.html",{"n":n})
        else:
            n="Email doesn't exist in our database"
            return render(request,"forgotpassword.html", {"n":n})