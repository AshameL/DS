# coding=utf-8
from win32com import client as wc
import os
import pythoncom
import re
from website.models import TestQuestion, User, Classes, Chapter
import xlrd, random, string
import logging


# 获取当前系统时间 需要输入格式
def getCurrentTime(format):
    import time
    return time.strftime(format, time.localtime(time.time()))


# 上传【doc或docx文件】,或【其他资料文件】
# f：文件名 directory：static下的某个指定文件夹
# 返回的 文件名不带路径 fileNameAddTimeRemoveSuffix + '.' + fileSuffixName
def handle_uploaded_file(f, directory):
    # 系统根路径
    filedirSystemRoot = os.path.dirname(__file__)
    # 系统根路径 转换 \
    filedirSystemRoot = filedirSystemRoot.replace('\\', '/')
    # 文件夹 static/【指定文件夹】
    filepathStaticDirectory = '/static/' + directory + '/'
    # 处理文件名
    temp = f.name.split('.')
    fileSuffixName = temp[-1]
    fileNameAddTimeRemoveSuffix = ""
    for i in range(0, len(temp) - 1):
        fileNameAddTimeRemoveSuffix += temp[i]
        fileNameAddTimeRemoveSuffix += '_'
    fileNameAddTimeRemoveSuffix += getCurrentTime('%Y%m%d_%H%M%S')
    filepathfilename = filedirSystemRoot + filepathStaticDirectory + fileNameAddTimeRemoveSuffix + '.' + fileSuffixName
    # 文件全路径
    print('上传文件：' + filepathfilename)

    # 写文件
    with open(filepathfilename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # media 课件等参考资料
    # reference 则跳过，学习课件不需要转换为html
    if directory == 'media':
        # 保存为html
        return saveAsHTML(filepathfilename)
    # 返回的 文件名不带路径
    return fileNameAddTimeRemoveSuffix + '.' + fileSuffixName


# 保存为HTML文件
def saveAsHTML(filename):
    pythoncom.CoInitialize()
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(filename)
    # 没有后缀名的前部分
    filenameFirstPart = filename.split('.')[0]
    doc.SaveAs(filenameFirstPart + '.html', 10)
    doc.Close()
    word.Quit()
    os.remove(filename)
    return filenameFirstPart + '.html'


# 队列 全部出列
def popall(list):
    ret = ''
    for i in list:
        ret += (i + '\n')
    ret = ret[:len(ret) - 1]
    list = []
    return ret, list


# 处理表格，并且为表格添加 class样式
def handle_table(table, tableclass):
    for (k, v) in table.items():
        #  print(k + '___' + v)
        v = re.sub(r'<span .*?>', '', v)  # 去掉<span  >
        v = re.sub(r'<p .*?>', '', v)  # 去掉<span  >
        v = re.sub(r'</span>', '', v)  # 去掉</span>
        v = re.sub(r'</p>', '', v)  # 去掉</span>

        v = re.sub(r'<td .*?>', '<td>', v)  # 去掉<span  >
        v = re.sub(r'<tr .*?>', '<tr >', v)  # 去掉<span  >
        v = re.sub(' ', '', v)
        if tableclass != '' or tableclass is None:
            v = re.sub(r'<table.*?>', '<table ' + tableclass + '>', v)  # 去掉<span  >
        else:
            v = re.sub(r'<table.*?>', '<table> ', v)  # 去掉<span  >
        table[k] = v
    # print(table)
    return table


# 处理img 返回line
def handle_img(line):
    # 替换掉字符串
    pattern = r'<img .*? src=.*?>'
    line = re.sub(pattern, r'<img src=.*?>', line)
    # 处理img src的文件
    r_img = r'<img src="(.*?)">'
    img_path_filename = re.findall(r_img, line)
    for img in img_path_filename:
        # spilt 分割文件名
        file = img.split(r'/')
        filepath = file[0]
        filename = file[-1]
        # 拼接文件路径，将文件复制
        # 删除源文件
        # repalce掉img
        img_filename = '<img src="' + img + '>'
    # 删除文件夹，再return
    return line


# 洗掉<p>内容多余个格式和标签
# m_p 是p主要内容list
# table_dict 是处理的表格内容的字典
# 返回 text_line
def handle_p_list_without_style(m_p, table_dict):
    text_line = []
    for m in m_p:
        line = ''
        output = re.sub(r'<span .*?>', '', m)  # 去掉<span  >
        output = re.sub(r'</span>', '', output)  # 去掉</span>
        output = re.sub('&nbsp;', '', output)  # 去掉 &nbsp;
        output = re.sub('（', '（', output)  # （）中文括号换英文
        output = re.sub('）', '）', output)  # （）中文括号换英文
        # 替换表格中随机字符串
        temp = []
        if m in table_dict.keys():
            for (k, v) in table_dict.items():
                output = re.sub(k, v, output)  # 去掉 &nbsp;
                temp.append(k)
            for t in temp:
                table_dict.pop(t)
        if output == '\n' or output == '':
            continue
        line += output
        # =====================
        text_line.append(line)
        # print(line)
        # print('table_dict')
        # print(table_dict)  # 这里看看table_dict 的内容
    return text_line


# 识别html  写入数据库
def readAndWriteDB(text_line):
    # 实例化
    info = TestQuestion()
    # 设置一个暂存文件行的栈区
    queue = []
    # 逐行读入，分析数据，写入数据库
    for line in text_line:
        if re.compile(r'^A').search(line):
            (info.content, queue) = popall(queue)
            queue.append(line)

        elif re.compile(r'^B').search(line):
            (info.A, queue) = popall(queue)
            queue.append(line)

        elif re.compile(r'^C').search(line):
            (info.B, queue) = popall(queue)
            queue.append(line)

        elif re.compile(r'^D').search(line):
            (info.C, queue) = popall(queue)
            queue.append(line)

        elif re.compile(r'^答案').search(line):
            if info.C is None or info.C == '':
                (info.C, queue) = popall(queue)
            else:
                (info.D, queue) = popall(queue)
            info.answer = re.findall(r'([A|B|C|D])', line)[0]
        elif re.compile(r'^知识点').search(line):
            know = re.split(r'：|:', line)[-1].strip()
            info.knowledge = know
        elif re.compile(r'^难度').search(line):
            diff = re.findall(r'(\d+)', line)[0]
            info.difficult = diff
        elif re.compile(r'^章节').search(line):
            # 添加try模块
            chapId = re.findall(r'(\d+)', line)[0]
            try:
                info.chapter = Chapter.objects.get(chap_id=chapId)
            except Exception as e:
                info.chapter = Chapter.objects.get(chap_id='0')
                logging.info(e)

            finally:
                info.save()
            if len(queue) != 0:
                logging.exception("异常queue的值：")
                logging.info(queue)
                queue = []
            # save new
            info = TestQuestion()
        else:
            queue.append(line)
            # 【缩进处理】处理 img 复制出新文件 删除源文件 修改稿line的引用内容
            # if re.compile(r'<img').search(line):
            #   line = handle_img(line)


def regexHTMLandWriteDB(filename, classStyleName):
    htmlfiletemp = open(filename, 'r')
    htmlfile = htmlfiletemp.read()
    # 替换掉所有换行以免干扰正则匹配
    htmlfile = htmlfile.replace('\n', ' ')

    # 记录表格的字典
    table_dict = {}
    res_table = r'<table .*?> .*? </table>'
    table_raw_data = re.findall(res_table, htmlfile)
    for i in table_raw_data:
        # 添加到表格字典中
        key = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        table_dict[key] = i
        key = r'<p class=MsoNormal>' + key + '</p>'

        # 替换 htmlfile
        htmlfile = htmlfile.replace(i, key)
    # 匹配<p> 标签内容
    res_p = r'<p class=MsoNormal.*?>(.*?)</p>'
    m_p = re.findall(res_p, htmlfile)

    # 处理table_dict
    table_dict = handle_table(table_dict, classStyleName)
    # 处理p标签中的多余格式
    text_line = handle_p_list_without_style(m_p, table_dict)
    readAndWriteDB(text_line)


# ##上传xls或xlsx文件,或其他资料文件
def handle_uploaded_xls_student(f):
    list_return = []
    filedir = os.path.dirname(__file__)
    filedir = filedir.replace('\\', '/')
    filepath = '/static/'  # 指定文件路径
    filepathfilename = filedir + filepath + f.name.split('.')[0] + getCurrentTime('_%Y%m%d_%H%M%S') + '.' + \
                       f.name.split('.')[-1]
    print(filepathfilename)
    with open(filepathfilename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # 识别 并写入 数据库
    # 删除掉表头
    data = xlrd.open_workbook(filepathfilename)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    # 写入数据库
    ################### 抛出异常
    for i in range(0, nrows):
        user = User()
        user.username = table.cell(i, 0).value
        user.name = table.cell(i, 1).value
        myclassname = table.cell(i, 2).value
        myclassname = myclassname.replace(' ', '')
        # Classes.objects.get_or_create(classname=myclassname)
        try:
            user.myclass = Classes.objects.get(classname=myclassname)
            # 不需要rollback
        except Exception as e:
            print(e)
            user.myclass = Classes.objects.create(classname=myclassname)
            print("创建班级" + user.myclass.classname)
            list_return.append("创建班级" + user.myclass.classname)

        user.headImage = '//'
        # 默认密码
        user.password = 'e10adc3949ba59abbe56e057f20f883e'  # 123456
        user.type = 1
        try:
            user.save()
        except Exception as e:
            # 存在了
            print(e)
            print(user.name + '(' + user.username + ')' + "已经存在")
            list_return.append(user.name + '（' + user.username + '）' + "已经存在")

    # 删除临时文件
    list_return.append("上传完毕")
    os.remove(filepathfilename)
    return list_return
