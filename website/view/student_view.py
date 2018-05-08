from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import json
from website.util_tool import *
from django.core import serializers
from django.http import StreamingHttpResponse

##########################################################################################################
# 学生主页
def student(request):
    return render(request, 'student/index.html')


# 学生：做题测试 列表
def test(request):
    # 知识点
    list = TestQuestion.objects.values_list('knowledge', flat=True).distinct()
    # list2 = TestQuestion.objects.values_list('chapter', flat=True).order_by('chapter').distinct()
    # 章节
    list2 = Chapter.objects.all().distinct()
    print(list2)
    return render(request, 'student/test_list.html', {'list_know': list, 'list_chapter': list2})


# 按照章节答题
# 生成成绩单
def test_chapter(request, chap, id):
    # chap 不在session中或者chap变了。重新取值
    # 如果session中有内容：继续取出所有值chap answer
    if 'chap' in request.session and request.session['chap'] == chap:
        testlist = request.session['testlist']
        chap = request.session['chap']
        answer = request.session['answer']
    else:  # 重新写入session
        # 按条件取出list
        if chap.isdigit():
            # 访问chapter
            chap_select = Chapter.objects.get(id=chap)
            testlist = TestQuestion.objects.filter(chapter=chap_select)
            chap = str(chap_select.chap_id)
        else:
            testlist = TestQuestion.objects.filter(knowledge=chap)
        listlen = len(testlist)
        # 对取出的list序列化
        testlist = serializers.serialize('json', testlist)

        # 实例化我的答案
        answer = []
        for i in range(listlen):
            answer.append("i")

        # 写入session中
        request.session['testlist'] = testlist
        request.session['chap'] = chap
        request.session['answer'] = answer
    testlist = testlist.encode().decode('unicode_escape')
    # 2017-09-09 处理\n
    testlist = json.loads(testlist, strict=False)
    testNow = testlist[int(id)]['fields']

    answerNow = answer[int(id)]
    if request.method == 'POST':
        answerNow = request.POST['select']
        # 写入answer中
        answer = request.session['answer']
        answer[int(id)] = answerNow
        request.session['answer'] = answer

    # 补充：点击确认提交表单时，取session grade，添加新值
    # grade中填过答案的绿色，空白的红色。加超链接
    return render(request, 'student/testing.html', {'testNow': testNow, 'chap': chap, 'length': len(testlist),
                                                    'id': int(id) + 1, 'answerNow': answerNow, 'answer': answer})


# 资料下载
def filedownload(request):
    from website.models import ReferenceFile
    # info = ReferenceFile.objects.all()
    info = ReferenceFile.objects.order_by('-uploadtime')

    # for i in info:
    #     suffix.append(i.filename.split('.')[-1])
    return render(request, 'student/filedownload.html', {'info': info})


# 下载文件#############################存在文件名下载问题########################################
def big_file_download(request, fileid):
    from website.models import ReferenceFile
    # 写入文件
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    filedir = os.path.dirname(__file__)
    filedir = filedir.replace('\\', '/')

    file = ReferenceFile.objects.get(id=fileid)
    the_file_name = file.path
    all_file_name = filedir + the_file_name
    print(all_file_name)
    print(file.filename)
    response = StreamingHttpResponse(file_iterator(all_file_name))
    filename = file.filename
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


# 提交成绩
def submitgrade(request):
    from website.models import Grade, ErrorQue
    testlist = request.session['testlist']
    testlist = testlist.encode().decode('unicode_escape')
    testlist = json.loads(testlist)
    answer = request.session['answer']
    correct = []
    testidlist = []
    for i in testlist:
        correct.append(i['fields']['answer'])
        # print(i)
        testidlist.append(i['pk'])
    # 创建成绩单对象

    # session 获取用户id
    chap = request.session['chap']
    u = request.session['userid']
    print(u)
    if chap.isdigit():
        chap = "第" + chap + "章"
    mygrade = Grade.objects.create(userid=User.objects.get(username=u), chapter=chap, accuracy=0)
    correct_num = 0
    for i in range(0, len(correct)):
        # 对比正确答案
        print(answer[i] + "----" + correct[i])
        # 跟正确答案相同
        if answer[i] == correct[i]:
            correct_num += 1
        else:  # 不同 生成错题对象
            print(type(answer[i]))
            ErrorQue.objects.create(gradeid=mygrade, testid=TestQuestion.objects.get(id=testidlist[i]),
                                    erroranswer=answer[i], count=1)
    accuracy = correct_num / len(answer)
    mygrade.accuracy = accuracy
    mygrade.save()

    return HttpResponseRedirect('/gradeslist/')


# 成绩
def grade(request):
    # 检查session，判断对错并写入系统。最后删除session
    from website.models import User, Grade
    user = request.session['userid']
    u = User.objects.get(username=user).id
    gradelist = Grade.objects.filter(userid=u)
    return render(request, 'student/grades.html', {'gradelist': gradelist})


# 成绩单详情
def gradedetails_stu(request, tid):
    from website.models import Grade, ErrorQue
    grade = Grade.objects.get(id=tid)
    errorque = ErrorQue.objects.filter(gradeid=tid)
    return render(request, 'student/gradedetails.html', {'grade': grade, 'error': errorque})


# 公告
def announce(request):
    from website.models import Announcement
    info = Announcement.objects.order_by('-briefReleaseTime')
    return render(request, 'student/announce.html', {'info': info})


# 我的账号
def mycount(request):
    return render(request, 'student/mycount.html')
