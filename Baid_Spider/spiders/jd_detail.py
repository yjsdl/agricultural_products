# -*- coding: utf-8 -*-
import json
import random

from urllib.parse import quote
import requests
import base64
import re
import os
import time
import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#
# chrome_options = Options()
# chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
# browser = webdriver.Chrome(executable_path=r'D:\python38\chromedriver.exe',
#                            options=chrome_options)  # executable执行webdriver驱动的文件





def get_msg(name, url, page):
    chrome_options = Options()  # 创建options对象
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('log-level=2')  # 日志级别
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')
    browser = webdriver.Chrome(r'D:\python38\chromedriver.exe', options=chrome_options)  # 打开chromedriver
    browser.maximize_window()
    browser.get(url)
    time.sleep(2)
    html = browser.page_source
    path = fr'F:\农产品搜索指数\Baid_Spider\京东大米\大米页面\{name}\\'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + str(page) + '.html', 'w', encoding='utf-8') as f:
        f.write(html)
    # res = etree.HTML(html)
    # 商品名称
    # shop_name = res.xpath('//')
    browser.close()
    browser.quit()






if __name__ == '__main__':
    pf1 = pd.read_csv('F:\农产品搜索指数\Baid_Spider\地理标识.csv', dtype=str)
    sha1 = pf1.shape[0]
    for i in range(1, 2):
        name = pf1.values[i][1]
        logo = pf1.values[i][2]
        path = fr'F:\农产品搜索指数\Baid_Spider\地理产品大米\{name}.csv'
        pf = pd.read_csv(path, dtype=str)
        sha = pf.shape[0]
        page = 1
        for j in range(1, sha):
            time.sleep(random.randint(8, 12))
            url = pf.values[j][1]
            summary = pf.values[j][3]
            print(url)
            if logo in summary:
                get_msg(name, url, page)
                page += 1

# 获取优惠券：https://item-soa.jd.com/getWareBusiness
"""jQuery" + Math.floor(1e7 * Math.random())"""