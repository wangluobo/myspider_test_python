#!/usr/bin/python
#-*- coding:utf-8 -*-
#test
import re
import urllib.request
import time
import urllib.error

headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0")
opener = urllib.request.build_opener()
opener.addheaders=[headers]
urllib.request.install_opener(opener)
listurl=[]#用来存放文章网址列表
#自定义函数,功能是使用代理服务器
def use_proxy(url):
    try:
        data = urllib.request.urlopen(url).read().decode('utf-8','ignore')
        return data
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        time.sleep(10)
def getlisturl(key,pagestart,pageend):
    try:
        page = pagestart
        #编码关键字KEY
        keycode=urllib.request.quote(key)
        #编码"&page"
        pagecode=urllib.request.quote("&page")
        #循环爬取各页的文章链接
        for page in range(pagestart,pageend+1):
            #构建各页的url连接
            url="http://weixin.sogou.com/weixin?type=2&query="+keycode+pagecode+str(page)
            #用代理服务器爬取,解决封杀IP问题
            data1= use_proxy(url)
            listurlpat=re.compile(r'<div class="txt-box">.*?href="(http://.*?)"',re.S)
            listurl.append(listurlpat.findall(data1))
        print("共获取"+str(len(listurl))+"页")
        print(listurl)
        return listurl
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        time.sleep(6)
    except Exception as e:
        print("exception:"+str(e))
        time.sleep(1)
# 通过文章链接获取对应内容
def getcontent(listurl):
    i =0
    #设置本地文件中的开始htnl编码
    html1='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>微信文章页面</title>
    </head>
    <body>    '''
    fh = open("D:/python/myweb/5.html","wb")
    fh.write(html1.encode("utf-8"))
    fh.close()
    #再次以追加的方式打开文件,以写入对应的文章内容
    fh=open("D:/python/myweb/5.html","ab")
    for i in range(0,len(listurl)):
        for j in range(0,len(listurl[i])):
            try:
                url=listurl[i][j]
                url=url.replace("amp;","")
                #使用代理去爬取对应的内容
                data=use_proxy(url)
                #文章标题正则表达式
                titlepat =re.compile(r"<title>(.*?)</title>")
                #文章内容正则表达式
                contentpat=re.compile(r'id="js_content">(.*?)</div>',re.S)
                #通过对应正则表达式找到找到标题并赋予给列表title
                title=titlepat.findall(data)
                #通过对应正则表达式找到内容并赋给列表content
                content=contentpat.findall(data)
                #初始化标题与内容
                thistitle="此次没有获取到"
                thiscontent="此次没有获取到"
                #如果标题列表不为空,说明找到了标题,取列表第零个元素,即此次标题赋给thistitle
                if(title!=[]):
                    thistitle=title[0]
                if(content!=[]):
                    thiscontent=content[0]
                #将标题与内容汇总赋给变量dataall
                dataall="<p>标题为:"+thistitle+"</p><p>内容为:"+thiscontent+"</p><br>"
                fh.write(dataall.encode("utf-8"))
                print("第"+str(i)+"个网页第"+str(j)+"次处理") #确定目前的爬的进程
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
                time.sleep(10)
            except Exception as e:
                print("exception:"+str(e))
                #Exception异常时,延时1秒执行
                time.sleep(1)
    fh.close()
    html2='''</body>
            </html>
            '''
    fh=open("D:/python/myweb/5.html","ab")
    fh.write(html2.encode("utf-8"))
    fh.close()
key="物联网"
pagestart=1
pageend=2
listurl=getlisturl(key,pagestart,pageend)
getcontent(listurl)








