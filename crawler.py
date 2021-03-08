#@Time:3/8/20212:19 PM
#@Author: Mini(Wang Han)
#@Site:
#@File:crawler.py
'''
目标:获取https://www.cnyes.com/usastock/stocks/NASDAQ.html
NASDAQ 使用當日開盤價; High: 當日最高價; Low: 當日最低價; Close: 當日收盤價; 成交量(Volume), 調整後股價(Adjust);
'''
import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

for m in range(1,208):
    url3 = 'https://app.quotemedia.com/quotetools/clientForward?targetURL=https%3A%2F%2Fstage.cnyes.com%2Fusastock%2FHistoryQM.aspx%3Fcode%3DCOMP&targetsym=&targettype=&targetex=&qmpage=true&action=showHistory&symbol=COMP&page=' + str(
        m) + '&startDay=1&startMonth=0&startYear=2001&endDay=31&endMonth=11&endYear=2020&perPage=25 '
    bs = webdriver.Chrome(r"G:\projects\Po\crawler\chrome\chromedriver.exe")
    bs.get(url3)
    bs.maximize_window()
    for i in range(0, 1):
        bs.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        time.sleep(1)
        bs.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        time.sleep(1)
        bs.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        time.sleep(1)
        bs.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        time.sleep(1)
        bs.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        time.sleep(1)
        print("finish scroll to the end ", str(i), "times")
    # html3 = urllib.request.urlopen(url3).read().decode('utf-8')
    html3 = bs.page_source
    soup3 = BeautifulSoup(html3, 'lxml')

    # 获取数据
    result32 = soup3.find_all(attrs={"class": "qm_history_historyContent"})
    result32 = str(result32)
    soup32 = BeautifulSoup(result32, 'lxml')

    result33 = soup32.find_all(attrs={"class": "qm_maintext"})
    item = {}
    item['date'] = []
    item['open'] = []
    item['high'] = []
    item['low'] = []
    item['close'] = []
    item['volume'] = []
    item['adjust'] = []
    for j in range(1, 26):
        i = j * 11
        item['date'].append(result33[i].string.replace(" ", ""))
        item['open'].append(result33[i + 1].string.replace(" ", ""))
        item['high'].append(result33[i + 2].string.replace(" ", ""))
        item['low'].append(result33[i + 3].string.replace(" ", ""))
        item['close'].append(result33[i + 4].string.replace(" ", ""))
        item['volume'].append(result33[i + 10].string.replace(" ", ""))
        item['adjust'].append(result33[i + 8].string.replace(" ", ""))
    print(item)

    '''
            数据库操作
    '''

    for i in range(0, len(item["date"])):
        date = item['date'][i]
        open = item['open'][i]
        high = item['high'][i]
        low = item['low'][i]
        close = item['close'][i]
        volume = item['volume'][i]
        adjust = item['adjust'][i]
        try:
            # 获取数据库链接
            connection = pymysql.connect(host="DESKTOP-D1AIO16", port=3307, user="mini", passwd="wangmianny111",
                                         db="stock_manager", charset='utf8')

            # 获取会话指针
            with connection.cursor() as cursor:
                # 创建sql语句
                sql = "insert into nasdaq (date,open,high,low,close,volume,adjust) values (%s,%s,%s,%s,%s,%s,%s)"

                # 执行sql语句
                cursor.execute(sql, (
                    date, open, high, low, close, volume, adjust))

                # 提交数据库
                connection.commit()
        finally:
            connection.close()
    print("sucess with page",m)


