# coding:utf-8

from django import forms


class UserLogForm(forms.Form):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class Announcement(forms.Form):
    from website import models

    SELECT_BOX_CHOICE = (('', '----请选择----'), ('资源公告', '资源公告'), ('作业公告', '作业公告'),
                         ('考试公告', '考试公告'), ('上课公告', '上课公告'),
                         ('其他公告', '其他公告'))
    classes = models.User.objects.values_list('myclass', flat=True).distinct()
    MULTIPLE_SELECT = []
    for myclass in classes:
        MULTIPLE_SELECT = MULTIPLE_SELECT + [(myclass, myclass)]

    briefTitle = forms.CharField(label='公告标题',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control col-md-7 col-xs-12', 'required': 'required'}))  # 标题
    briefContent = forms.CharField(label='公告内容',
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}))  # 内容
    briefClass = forms.MultipleChoiceField(label='可见班级', widget=forms.CheckboxSelectMultiple(), choices=MULTIPLE_SELECT)
    # 资源公告，作业公告，其他公告
    briefType = forms.CharField(label='公告类型',
                                widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'},
                                                    choices=SELECT_BOX_CHOICE))  # 可见班级


# 文件上传
class FileUpload(forms.Form):
    CHOICE_BOX_CHOICE = (('校内', '校内可见'), ('校外', '校外可见'), ('全部', '全部可见'))
    filename = forms.FileField()
    # visibleRange = forms.ChoiceField(label='可见班级：', choices=CHOICE_BOX_CHOICE, widget=forms.RadioSelect())
    remark = forms.CharField(required=False)
    visibleRange = forms.CharField()


# 试题上传 学生名单上传 也在此
class TestingUpload(forms.Form):
    filename = forms.FileField()


# 修改试题
class EditTest(forms.Form):
    content = forms.CharField()
    A = forms.CharField()
    B = forms.CharField()
    C = forms.CharField()
    D = forms.CharField()
    answer = forms.CharField()
    chapter = forms.CharField()
    knowledge = forms.CharField()
    difficult = forms.CharField()

# 答题
# class Testing(forms.Form):
