from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import json
from website.forms import *
import hashlib
from website.util_tool import *
from django.core import serializers
from django.http import StreamingHttpResponse
from django.shortcuts import redirect


# from django.contrib import messages


# 登录处理
def login(request):
    from website import models
    from django.core.exceptions import ObjectDoesNotExist
    if request.method == 'POST':  # 表单提交时
        form = UserLogForm(request.POST)  # form 包含提交的数据
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            pw_md5 = hashlib.md5(p.encode(encoding='utf-8')).hexdigest()
            print(p + '：' + pw_md5)
            # 这里进行数据的验证
            '''if 老师  retrun进入老师界面
            if 学生 return 学生界面
            else 账号密码错误 尝试网页上动态验证
            取出老师用户名
                if 输入是否在其中，取出密码，验证密密码
                    if 对应 return 教师index，session赋值
                    else message.error 重新登录
                elif 是否在学生中，try 存在异常
                    if 对应 return 学生index，session赋值
                    else message.error 密码错误
                else message.error 用户名不存在
            '''
            teacherNameList = models.Teacher.objects.values_list('teachername', flat=True)
            if u in teacherNameList:
                if pw_md5 == models.Teacher.objects.get(teachername=u).teacherpassword:
                    request.session['username'] = u
                    return redirect('/tea_index/')
                else:  # 密码错误
                    errorMessages = 'T密码错误'
                    return render(request, 'login.html', {'errorMessages': errorMessages})
            # 判断学生
            else:
                try:
                    student = models.User.objects.get(username=u)
                    if student.password == pw_md5:
                        # 添加session
                        request.session['username'] = student.name
                        request.session['userid'] = student.username
                        request.session['userimg'] = student.headImage
                        return redirect('/index/')

                    else:
                        print('学生密码错误')
                        errorMessages = '学生密码错误'
                        return render(request, 'login.html', {'errorMessages': errorMessages})

                except ObjectDoesNotExist as e:

                    print('用户名不存在')
                    print(e)
                    errorMessages = '用户名不存在'
                    return render(request, 'login.html', {'errorMessages': errorMessages})

    else:
        form = UserLogForm()
        errorMessages = ''
        return render(request, 'login.html', {'form': form, 'errorMessages': errorMessages})


# 注册
def register(request):
    from django.core.exceptions import ObjectDoesNotExist
    from website import models
    if request.method == 'POST':  # 表单提交时
        form = UserLogForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            pw_md5 = hashlib.md5(p.encode(encoding='utf-8')).hexdigest()
            print('pw_md5:' + pw_md5)
            try:
                models.User.objects.get(username=u)
            except ObjectDoesNotExist:
                user = User()
                user.name = u
                user.username = u
                user.password = pw_md5
                user.myclass = '校外'
                user.type = 2
                user.headImage = '//'
                user.save()
                # 登录到新页面中
                return render(request, 'teacher/t_index.html')
            return HttpResponse('error register')


# 登出。注销
def logout(request):
    del request.session['username']
    return redirect('/login/')


# 编辑试题
def test_edit(request, tid):
    from website import models
    info = models.TestQuestion.objects.get(id=tid)
    if request.method == 'POST':
        my_form = EditTest(request.POST)
        if my_form.is_valid():
            info.content = my_form.cleaned_data['content']
            info.A = my_form.cleaned_data['A']
            info.B = my_form.cleaned_data['B']
            info.C = my_form.cleaned_data['C']
            info.D = my_form.cleaned_data['D']
            info.difficult = my_form.cleaned_data['difficult']
            info.answer = my_form.cleaned_data['answer']
            info.chapter = my_form.cleaned_data['chapter']
            info.knowledge = my_form.cleaned_data['knowledge']
            info.save()

    return render(request, 'teacher/t_que_edit.html', {'info': info})


# 删除试题
def test_delete(request, tid):
    from website import models
    models.TestQuestion.objects.get(id=tid).delete()
    # 重定向返回本页面
    return HttpResponseRedirect('/tea_question/')


# 查看试题
def test_view(request, tid):
    from website import models
    info = models.TestQuestion.objects.get(id=tid)
    return render(request, 'teacher/t_que_view.html', {'info': info})


# bootstrap
def bootstrap(request):
    # return ;
    return render(request, 'student/student_base.html')


def delete_file(request, tid):
    from website.models import ReferenceFile
    # 删除文件存储位置
    info = ReferenceFile.objects.get(id=tid)
    filedir = os.path.dirname(__file__)
    filedir = filedir.replace('\\', '/')
    path = info.path
    os.remove(filedir + '/' + path)
    # 删除数据库
    ReferenceFile.objects.get(id=tid).delete()
    return redirect('/tea_file/')


def secret(request, tid):
    from website.models import User
    info = User.objects.get(id=tid)


def headimg(requset, tid):
    pass


def grades(request):
    from website.models import Grade
    gradelist = Grade.objects.order_by('-time')

    return render(request, 'teacher/t_grades.html', {'gradelist': gradelist})


def gradedetails(request, tid):
    from website.models import Grade, ErrorQue
    grade = Grade.objects.get(id=tid)
    errorque = ErrorQue.objects.filter(gradeid=tid)
    return render(request, 'teacher/t_gradedetails.html', {'grade': grade, 'error': errorque})


def chapter(request):
    return render(request, 'teacher/t_chapter.html')
