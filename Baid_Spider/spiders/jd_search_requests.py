# -*- coding: utf-8 -*-
# @date：2022/12/6 10:20
# @Author：crab-pc
# @file： jd_search_requests

import requests
import os
import random
import pandas as pd
import UserAgent

class JDRequest:

    def __init__(self):
        self.headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
    }

    def first_requests(self):
        pf = pd.read_csv(r'F:\农产品搜索指数\Baid_Spider\地理标识.csv', dtype=str)
        sha = pf.shape[0]
        i1 = 40
        for i in range(i1, i1 + 1):
            # mi_name = pf.values[i][1]
            # keyword = pf.values[i][2]
            mi_name = '比德大米'
            keyword = '比德'
            print(mi_name, keyword)
            params = {
                'keyword': keyword,
                'wq': keyword,
                'cid3': 2675
            }
            url='https://search.jd.com/Search'
            refer = f'https://search.jd.com/search?keyword={keyword}&wq={keyword}&cid3=2675'
            meta = dict(keyword=keyword, mi_name=mi_name, refer=refer, page=1)
            headers = self.headers.copy()
            headers['User-Agent'] = random.choice(UserAgent.fake_useragent())
            res = requests.get(url=url, params=params, headers=headers)