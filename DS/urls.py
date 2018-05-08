"""DS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from website import views as web_view
from website.view import teacher_view as t_view
from website.view import student_view as s_view
 
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', web_view.login, name='login'),
    url(r'^#$', web_view.login, name='login'),
    # 注销
    url(r'logout/', web_view.logout, name='logout'),
    url(r'^/#signup$', web_view.register, name='register'),
    # 教师-----------------------------------------------------
    # 基础功能
    url(r'^tea_index/', t_view.teacher, name='tea_index'),
    # announce 公告声明
    url(r'^tea_ann/$', t_view.tea_annou, name='tea_ann'),
    url(r'^tea_ann/edit/(\d+)', t_view.tea_ann_edit, name='tea_ann_edit'),
    url(r'^tea_ann/delete/(\d+)', t_view.tea_ann_delete, name='tea_ann_delete'),

    url(r'^tea_question/$', t_view.upload_test, name='tea_question'),
    url(r'^tea_chapter/$', web_view.chapter, name='tea_chapter'),
    # 对试题的修改 查看 删除 2017-05-02
    url(r'^tea_question/delete/(\d+)/$', web_view.test_delete, name='tea_question_delete'),
    url(r'^tea_question/view/(\d+)/$', web_view.test_view, name='tea_question_view'),
    url(r'^tea_question/edit/(\d+)/$', web_view.test_edit, name='tea_question_edit'),

    url(r'^tea_file/', t_view.upload_file, name='tea_file'),
    url(r'^tea_file_del_(\d+)', web_view.delete_file, name='tea_file_del'),

    url(r'^tea_manage/', t_view.manage, name='tea_manage'),
    # 查看成绩
    url(r'^tea_grades/$', web_view.grades, name='tea_grades'),
    url(r'^tea_grades/(\d+)', web_view.gradedetails, name='tea_gradesdetails'),

    url(r'^bootstrap/', web_view.bootstrap),
    # 修改教师密码
    url(r'^password/', t_view.changepassword, name='password'),
    # 学生------------------------------------------------------------------------------------------------------------------
    # 做题，测试
    url(r'^index', s_view.student, name='s_index'),
    url(r'^testing/(\d+)/(\d+)/$', s_view.test_chapter, name='testQue2'),
    url(r'^testing/(.*?)/(\d+)/$', s_view.test_chapter, name='testQue'),
    url(r'^testlist/$', s_view.test, name='testlist'),
    # 成绩单
    url(r'^submitgrade/$', s_view.submitgrade, name='submitgrade'),
    url(r'^gradeslist/$', s_view.grade, name='gradeslist'),
    url(r'^gradeslist/(\d+)', s_view.gradedetails_stu, name='grade_detail_student'),

    # 资料下载
    url(r'^filedownload/$', s_view.filedownload, name='filedownload'),
    url(r'^filedownload/(\d+)', s_view.big_file_download, name='downlaod'),
    # 查看公告
    url(r'^announce/$', s_view.announce, name='announce'),
    # 我的账号
    url(r'mycount/$', s_view.mycount, name='mycount'),

]
