import threading,queue
import re, time
import urllib.request
import urllib.error

#获取文章连接的队列
urlqueue= queue.Queue()

#模拟浏览器
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0")
opener= urllib.request.build_opener()
opener.addheaders=[headers]
#安装为全局
urllib.request.install_opener(opener)
listurl=[]
#获取网页数据
def use_urlopen(url):
    try:
        data =urllib.request.urlopen(url).read().decode('utf-8','ignore')
        return data
    except urllib.error.URLError as e :
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        time.sleep(7)
    except Exception as e:
        print("exception:"+str(e))
        time.sleep(1)
#线程1,专门获取对应网址并处理为真实网址
class geturl(threading.Thread):
    def __init__(self,key,pagestart,pageend,urlqueue):
        threading.Thread.__init__(self)
        self.pagestart=pagestart
        self.pageend=pageend
        self.urlqueue=urlqueue
        self.key=key
    def run(self):
        page=self.pagestart
        keycode=urllib.request.quote(key)
        pagecode=urllib.request.quote("&page")
        for page in range(self.pagestart,self.pageend+1):
            url="http://weixin.sogou.com/weixin?type=2&query="+keycode+pagecode+str(page)

            data1=use_urlopen(url)#获取要爬取的网页数据
            #列表页url正则
            listurlpat = re.compile(r'<div class="txt-box">.*?href="(http://.*?)"', re.S)
            listurl.append(listurlpat.findall(data1))
        print("获取到"+str(len(listurl))+"页")
        for i in range(0,len(listurl)):
            #等一等线程2,合理分配资源
            time.sleep(5)
            for j in range(0,len(listurl[i])):
                try:
                    url=listurl[i][j]
                    url=url.replace("amp;","")
                    print("第"+str(i)+"i"+str(j)+"j次写入队")
                    self.urlqueue.put(url)
                    self.urlqueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e,"code"):
                        print(e.code)
                    if hasattr(e,"reason"):
                        print(e.reason)
                    time.sleep(10)
                except Exception as e:
                    print("exception:"+str(e))
                    time.sleep(1)
class getcontent(threading.Thread):
    def __init__(self,urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue=urlqueue
    def run(self):
        html1 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
           <html xmlns="http://www.w3.org/1999/xhtml">
           <head>
           <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
           <title>微信文章页面</title>
           </head>
           <body>    '''
        fh = open("D:/python/myweb/6.html", "wb")
        fh.write(html1.encode("utf-8"))
        fh.close()
        fh = open("D:/python/myweb/6.html", "wb")
        i =1
        while(True):
            try:
                url=self.urlqueue.get()
                data=use_urlopen(url)
                contentpat=re.compile(r'id="js_content">(.*?)</div>',re.S)
                titlepat=re.compile(r'<title>(.*?)</title>')
                # 通过对应正则表达式找到找到标题并赋予给列表title
                title = titlepat.findall(data)
                # 通过对应正则表达式找到内容并赋给列表content
                content = contentpat.findall(data)
                # 初始化标题与内容
                thistitle = "此次没有获取到"
                thiscontent = "此次没有获取到"
                # 如果标题列表不为空,说明找到了标题,取列表第零个元素,即此次标题赋给thistitle
                if (title != []):
                    thistitle = title[0]
                if (content != []):
                    thiscontent = content[0]
                # 将标题与内容汇总赋给变量dataall
                dataall = "<p>标题为:" + thistitle + "</p><p>内容为:" + thiscontent + "</p><br>"
                fh.write(dataall.encode("utf-8"))
                print("第" + str(i) + "个网页第"  + "次处理")  # 确定目前的爬的进程
                i+=1
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
                time.sleep(10)
            except Exception as e:
                print("exception:"+str(e))
                time.sleep(1)
        fh.close()
        html2='''</body>
        </html>'''
        fh = open("D:/python/myweb/6.html","wb")
        fh.write(html2.encode("utf-8"))
        fh.close()
class contrl_use(threading.Thread):
    def __init__(self,urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue=urlqueue
    def run(self):
        while(True):
            print("程序执行中")
            time.sleep(60)
            if(self.urlqueue.empty()):
                print("程序执行完毕")
                exit()
key="人工智能" #微信搜索关键字
pagestart=1 #起始页
pageend=3 #终点页
t1=geturl(key,pagestart,pageend,urlqueue)
t1.start()
t2=getcontent(urlqueue)
t2.start()
t3=contrl_use(urlqueue)
t3.start()

