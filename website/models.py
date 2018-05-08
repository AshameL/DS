# coding=utf8
from django.db import models


# Create your models here.
# 班级表
class Classes(models.Model):
    classname = models.CharField(max_length=16, unique=True)


# 用户表
class User(models.Model):
    username = models.CharField(max_length=16, unique=True)  # 用户表 学号
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=16)  # 用户名【主键】，密码 默认值：（data0structure1）
    # myclass = models.CharField(max_length=16, null=True, blank=True)  # 所属班级 校外为空
    myclass = models.ForeignKey(Classes, null=True)
    headImage = models.CharField(max_length=255)  # 头像（存url） headImage中
    type = models.IntegerField()  # type：0老师，1学生，2外校人员


# 公告表
class Announcement(models.Model):
    briefTitle = models.CharField(max_length=64)  # 标题
    briefContent = models.CharField(max_length=1024)  # 内容
    briefReleaseTime = models.DateTimeField(auto_now=True)  # 时间类型，看在数据库中怎样保存### 时区是这样的吗
    briefClass = models.CharField(max_length=16)  # 可见班级 # 格式：1|2|3|5|1  空为所有人可见 学生为学生可见 校外可见
    briefType = models.CharField(max_length=16)  # 资源公告，作业公告，其他公告，等等


# 章节号，知识点对应表
class Chapter(models.Model):
    chap_id = models.IntegerField()
    chap_num = models.CharField(max_length=64)  # 章节的标题。与主键对应


class Knowledge(models.Model):
    know_name = models.CharField(max_length=128)
    know_chap = models.ForeignKey(Chapter)  # 关联的章节


# 测试试题表
class TestQuestion(models.Model):
    content = models.CharField(max_length=512)  # 题干
    A = models.CharField(max_length=128)  # 选项
    B = models.CharField(max_length=128)
    C = models.CharField(max_length=128, null=True)
    D = models.CharField(max_length=128, null=True)
    # chapter = models.IntegerField(null=True)  # 章节
    chapter = models.ForeignKey(Chapter)
    difficult = models.IntegerField(null=True)
    answer = models.CharField(max_length=2)  # 答案
    knowledge = models.CharField(max_length=16)  # 知识点，内容


# 上传资料表 参考资料
class ReferenceFile(models.Model):
    filename = models.CharField(max_length=32)  # 文件名
    uploadtime = models.DateTimeField(auto_now_add=True)  # 上传时间
    remark = models.CharField(max_length=64, null=True, blank=True)  # 备注
    path = models.CharField(max_length=128)
    suffix = models.CharField(max_length=12, null=True)
    visible = models.CharField(max_length=12, null=True)
    chapter = models.ForeignKey(Chapter, null=True)  # 章节可以为空，标识范围不限制


# 成绩单
class Grade(models.Model):
    userid = models.ForeignKey(User)
    chapter = models.CharField(max_length=32)  # 知识点，或者章节号
    accuracy = models.FloatField()
    time = models.DateTimeField(auto_now=True)


# 错题表
class ErrorQue(models.Model):
    gradeid = models.ForeignKey(Grade)
    testid = models.ForeignKey(TestQuestion)
    erroranswer = models.CharField(max_length=4)
    count = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


# 教师表
class Teacher(models.Model):
    teachername = models.CharField(max_length=16, unique=True)
    teacherpassword = models.CharField(max_length=32)
