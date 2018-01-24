# E:\python\CircularTranslation\A.txt

import os
import time
import random
import requests
from bs4 import BeautifulSoup

def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0'
                       ]
    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return header

def getCurrentTime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

def get_file_path():
    global path
    path = input('输入单词文件绝对路径：')
    return path

def translate_abc(word):
    # 利用有道翻译查询单词
    url = 'http://dict.youdao.com/w/{}/'.format(word)
    html = getURL(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    trans_container = soup.find(class_='trans-container')

    if not trans_container:
        return [word]

    trans_li = trans_container.find_all('li')
    trans_data = [li.text.strip() for li in trans_li]
    return trans_data

def getURL(url, tries_num=5, sleep_time=0, time_out=10, max_retry=5, isproxy=0, proxy=None, encoding='utf-8'):
    header = randHeader()
    try:
        res = requests.Session()
        if isproxy == 1:
            if proxy is None:
                print('===   proxy is empty     ====')
                return None
            res = requests.get(url, headers=header, timeout=time_out, proxies=proxy)
        else:
            res = requests.get(url, headers=header, timeout=time_out)
        res.raise_for_status()
    except requests.RequestException as e:
        if tries_num > 0:
            time.sleep(sleep_time)
            print(getCurrentTime(), url, 'URL Connection Error in ', max_retry - tries_num, ' try')
            return getURL(url, tries_num - 1, sleep_time + 10, time_out + 10, max_retry, isproxy, proxy)
        return None

    res.encoding = encoding  # 指定网页编码格式
    return res

def get_file_content():
    file = open(get_file_path()) # 原始单词文件
    for_file = open(path) # 循环输出单词文件
    # w_file = open(r'B-T.txt', 'w+') # 写入新的翻译后的文件
    line = len(file.readlines())
    file.seek(0)
    # w_file.seek(0)
    for_file.seek(0)

    print('\n\t模式：', file.mode, end='')
    print('\n\t路径：', file.name, end='')
    print('\n\t行数：', line, '\n')

    input('按任意键开始翻译！\n')

    ''' 妈的，保存文件想了那么久，不是空列表就是游标错位，把控制台输出的复制一遍不就行了嘛，哈哈哈 ~~~'''

    for i in range(line):
        print(str(i) + ':' + for_file.readline(), translate_abc(file.readline()))
        '''if len(translate_abc(file.readline())):
            save = str(i) + ":" + for_file.readline() + translate_abc(file.readline())[0] + '\n'
        else:  # 判断单词是否错误，因为返回的是 empty list 会退出程序
            save = str(i) + ":" + for_file.readline() + '这个单词翻译不出来
        w_file.write(save)'''
    print('\n')

if __name__ == '__main__':
    print('\n')
    print('Author：Turaiiao')
    print('Email：1171840237@qq.com')
    print('Url：https://xyiio.cn/', '\n')

    get_file_content()