import re
import urllib.request

user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
def craw(url,page):
    html1=urllib.request.urlopen(url).read()
    html1=str(html1)
    pat1='<div id="plist".+?<div class="page clearfix">'

    result1 = re.compile(pat1).findall(html1)
    result1 = result1[0]
    pat2 = re.compile(r'<img width="220" height="220" data-img="1"(.+?)>')  #进一步缩小范围
    result2=pat2.findall(result1)
    result2 = ' '.join(result2)
    pat3 = re.compile(r'src="//(.+?)"')#提取src的连接
    pat4 = re.compile(r'data-lazy-img="//(.+?)"') #提取data-lazy-img连接
    imagelist1= pat3.findall(result2)

    imagelist2= pat4.findall(result2)

    imagelist = imagelist1+imagelist2
    # print(imagelist)
    # imagelist0 =[]
    # for x in range(len(imagelist)):
    #     imagelist0.append(imagelist[x][0])
    #     imagelist0.append(imagelist[x][1])
    # #     imagelist0.remove('')
    # print(imagelist0)
    imageurltxt = open("D:/python/myweb/1.txt","w+")
    imageurltxt.write("\n".join(imagelist))
    imageurltxt.close()
    x=1
    for imageurl in imagelist:
        imagename="D:/python/myweb/img1/"+str(page)+str(x)+".jpg"
        imageurl = "http://"+imageurl
        try:
            urllib.request.urlretrieve(imageurl,filename=imagename)
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                x+=1
                print(e)
            if hasattr(e,"reason"):
                x+=1
                print(e)
        x+=1
for i in range(1,4):
    url = "https://list.jd.com/list.html?cat=9987,653,655&page="+str(i)
    craw(url,i)




