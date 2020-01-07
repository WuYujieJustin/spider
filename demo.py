from selenium import webdriver
import requests
from browsermobproxy import Server
import re
import textract

# from mitmproxy import ctx
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# server = Server(r'd:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
# server.start()
# proxy = server.create_proxy()

# chrome_options = Options()
# chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
# driver = webdriver.Chrome(ChromeDriverManager().install())
root_url = "http://ien.shou.edu.cn"
base_url = "http://ien.shou.edu.cn/2219/list.htm"
soup = {}

def init ():
    global soup
    r = requests.get(base_url)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text, 'lxml')
    getlist()

def gotonextpage ():
    global soup
    link = soup.find_all('a', 'next', limit=1)[0].get("href")
    if(re.search('htm', link) == None):
        return
    nextpagelink = root_url + link
    r = requests.get(nextpagelink)
    soup = BeautifulSoup(r.text, 'lxml')
    getlist()

def getlistdetail (link):
    r = requests.get(link)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text, 'lxml')
    pubdate = soup('span', 'Article_PublishDate')[0].get_text()
    viewcount = soup('span', 'WP_VisitCount')[0].get_text()
    title = soup('span', 'Article_Title')[0].get_text()
    content = soup('div', 'Article_Content', limit=1)[0]
    attach_file = soup.find_all(href=re.compile("_upload/article"))
    img = soup.find_all(src=re.compile("_upload/article"))
    gotonextpage()

def getlist ():
    global soup
    items = soup.find_all('a',href = re.compile("page"), limit=14)
    for n in items:
        title = n.get_text()
        herf = n.get("href")
        data = {
            '标题':title,   
            '链接':herf
        }
        link = root_url + herf
        getlistdetail(link)
init()
# text = textract.process("C:/Users/zhongbiao/Downloads/1.doc")
# text = text.decode("utf-8")
# print(text)

# server.stop()
# driver.quit()