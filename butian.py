import json,os
import requests
import time
import re
from bs4 import BeautifulSoup
headers = {
    'Origin': 'https://www.butian.net',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Host': 'www.butian.net',
    'Origin': 'https://www.butian.net',
    'Referer': 'https://www.butian.net/Reward/plan',
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
print("\033[1;33m正在获取总页数\033[0m")
try:
    res = requests.post('https://www.butian.net/Reward/pub',
                        headers=headers,
                        timeout=10)
    result = json.loads(res.text)
    total = result['data']['count']
except Exception:
    print("\033[1;33m总页数获取失败\033[0m")
    os._exit(0)
print("\033[1;33m总页数：{0}\033[0m".format(total))
def spider():
    '''
    :return:
    '''
    headers = {
        'Host': 'www.butian.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.butian.net/Reward/plan',
        'Cookie': '',#填自己cookie
        'Connection': 'keep-alive'
    }
    for i in range(1, total):
        try:
            data={
                's': '1',
                'p': i,
                'token': ''
            }
            time.sleep(1)
            res = requests.post('https://www.butian.net/Reward/pub', data=data,headers=headers,timeout=(4,20))
            allResult = {}
            allResult = json.loads(res.text)
            currentPage = str(allResult['data']['current'])
            currentNum = str(len(allResult['data']['list']))
            print('正在获取第' + currentPage + '页厂商数据')
            print('本页共有' + currentNum + '条厂商')
            # print(allResult)
            for num in range(int(currentNum)):
                base='https://www.butian.net/Loo/submit?cid='
                with open('id.txt','a') as f:
                    f.write(base+allResult['data']['list'][int(num)]['company_id']+'\n')
        except requests.ConnectionError :
            print("fail to open url ")
    time.sleep(5)
    count=len(open("id.txt",'r').readlines())
    print("\033[1;33m目前获取了：{0}个compid\033[0m".format(count))            

def Url():
    '''
    遍历所有的ID
    取得对应的域名
    保存为target.txt
    :return:
    '''    
    headers = {
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        }
    cookie = ''
    cookies={'btlc_ba52447ea424004a7da412b344e5e41a':cookie}
    with open('id.txt','r') as f:
        for target in f.readlines():
            target=target.strip()
            time.sleep(2)
            getUrl=requests.get(target,cookies=cookies,headers=headers)
            if re.findall('(?:"\svalue=")([\w\d\.\-\（\）\(\):/]+)(?:" />)',getUrl.text):
                src = re.findall('(?:"\svalue=")([\w\d\.\-\（\）\(\):/]+)(?:" />)',getUrl.text)
                try:
                    src_name = src[0]+':'+src[1]
                    src_url = src[1]+'\n'
                    print(src_name)
                    # print(src_url)
                    with open('target.txt','a') as t:
                        t.write(src_url)
                except:
                    print("error")
            else:
                continue

if __name__=='__main__':
    # f = open('id.txt','w')
    # f.truncate()
    # spider()
    Url()
