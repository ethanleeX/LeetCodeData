#coding=utf-8 
'''
author Jon Lee
date 8/9/2015
'''
import requests
from bs4 import BeautifulSoup
import os

#获得题目内容
def getProblemContent(href):
    url = 'https://leetcode.com' + href
    try:
        req = requests.get(url,headers = headers,timeout=20)
    except (requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout):#处理连接超时
        print('time out')
        return 'time out'
    
    problemPage = BeautifulSoup(req.text)
    questionContents = problemPage.select('.question-content')#找到存放题目的div
    contents = questionContents[0].find_all(['p','pre'])#找到所有p和pre标签
    contentText  = ''
    for content in contents:
        contentText += content.get_text()
    req.close()
    return contentText

#写入文件
def saveQuestion(content):
    #content['title'].replace(' ','_')#将空格替换成_
    name = content['id'] + '_' + content['title'] + '.txt'#文件名 id_title.txt  如 242_Valid Anagram.txt
    if not os.path.exists(name):#文件不存在 创建文件
        print('create',name)
        f = open(name,'wb+')#打开文件  准备写入
        f.write(content['content'].encode(encoding='utf_8'))#写入文件
        f.close()#关闭文件
        
#伪装成浏览器
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'}
r = requests.get('https://leetcode.com/problemset/algorithms/',headers = headers)
#print(r.status_code)
#print(r.text)
soup = BeautifulSoup(r.text)
#print(soup.title.string)

#找到题目所在位置
table = soup.find(id='problemList')
#题目信息存放在tbody的tr中  找出所有tr
tr = table.tbody.find_all('tr')
#找出其中免费题目  观察源码  没有i标签的即为免费题目
problemListEasy = []  #初始化列表  用于存放题目
problemListMedium = []  #初始化列表  用于存放题目
problemListHard = []  #初始化列表  用于存放题目

for problem in tr:
    if type(problem.find('i')) is type(None):
        #记录题目 id title link acceptance difficulity 以字典方式存入列表
        td = problem.find_all('td')
        p_id =td[1].string
        title = td[2].a.string
        link = td[2].a.get('href')
        acceptance = td[3].string
        difficulity = td[4].string
        
        #读取内容
        content = getProblemContent(link)
        #print(content)
        p_dict = {'id':p_id,'title':title,'content':content,'acceptance':acceptance,'difficulity':difficulity}
        print(p_dict['id'])
        #将问题根据难度放入不同列表
        if difficulity == 'Easy':
            problemListEasy.append(p_dict)
        elif difficulity == 'Medium':
            problemListMedium.append(p_dict)    
        else:
            problemListHard.append(p_dict)
            
#文件操作  创建存放题目的目录及文件
#切换路径
os.chdir('F:\ComputerRobotData')
if not os.path.exists('leetcode'):#目录不存在  则创建
    os.mkdir('leetcode')
    
os.chdir('leetcode')

#创建easy medium hard三个目录存放相应题目
if not os.path.exists('easy'):#目录不存在  则创建
    os.mkdir('easy')
if not os.path.exists('medium'):#目录不存在  则创建
    os.mkdir('medium')
if not os.path.exists('hard'):#目录不存在  则创建
    os.mkdir('hard')

#写入简单题
os.chdir('easy')
#print(problemListEasy)
for pEasy in problemListEasy:
    saveQuestion(pEasy)

#写入中等题
os.chdir('../medium')
#print(problemListMedium)
for pMedium in problemListMedium:
    saveQuestion(pMedium)

#写入困难题
os.chdir('../hard')
#print(problemListHard)
for pHard in problemListHard:
    saveQuestion(pHard)      
    
print('finish!!') 
    