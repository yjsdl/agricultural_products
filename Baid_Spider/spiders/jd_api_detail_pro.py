# -*- coding: utf-8 -*-
import requests
import pandas as pd
import os
import re
import time
import logging
from copy import deepcopy
from lxml import etree
import random
import UserAgent

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


class JdDetail:
    def __init__(self):

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
        }

    # 保存到csv文件
    def save_list(self, data, file, name):
        # desk = os.path.join(os.path.expanduser('~'), 'Desktop')
        # 当前文件夹
        file_path = r'F:\农产品搜索指数\Baid_Spider\京东大米\基本信息2\\' + file
        if os.path.isfile(file_path):
            df = pd.DataFrame(data=data)
            df.to_csv(file_path, encoding="utf-8", mode='a', header=False, index=False)
        else:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df = pd.DataFrame(data=data, columns=name)
            df.to_csv(file_path, encoding="utf-8", index=False)

    def first_requests(self):
        pf1 = pd.read_csv('F:\农产品搜索指数\Baid_Spider\地理标识.csv', dtype=str)
        sha1 = pf1.shape[0]
        for i in range(6, 7):
            # i = 18+
            i = 171

            # 117
            name = pf1.values[i][1]
            logo = pf1.values[i][2]
            path = fr'F:\农产品搜索指数\Baid_Spider\地理产品大米\{name}.csv'
            # path = r'F:\农产品搜索指数\Baid_Spider\京东大米\基本信息\五常大米.csv'
            pf = pd.read_csv(path, dtype=str).fillna('')

            sha = pf.shape[0]
            if sha == 0:
                data = []
                data.append(
                    {'商品名称': '', '商品店铺': '', '商品链接': '', '商品重量': '',
                     '商品价格': '', '商品视频': '', '优惠活动': '',
                     '京东物流': '',
                     '7天无理由': '', '企业品牌': '', '进出口': '',
                     '包装': '', '等级': '', '商品产地': '', '产品标准号': '',
                     '保质期': '', '绿色食品': '',
                     '地理标志产品': '', '有机产品': '', '溯源': '',
                     '全部评价': '', '好评度': '',
                     '晒图': '', '视频晒图': '', '好评': '', '中评': '',
                     '差评': ''})
                self.save_list(data, f'{name}.csv', data[0].keys())
            print(i, name, sha, logo)
            # 射阳 200-300
            for j in range(0, sha):
                url = pf.values[j][1]
                if url:
                    # url = 'https://item.jd.com/69824038332.html'
                    shop_name = pf.values[j][0]
                    price = pf.values[j][2]
                    summary = pf.values[j][3]
                    summary = summary.replace(' ', '')
                    meta = dict(name=name, price=price, shop_name=shop_name, url=url)
                    if logo in summary and (not re.search(r'酒', summary)) and (not re.search(r'糍粑', summary)) and (
                    not re.search(r'书', summary)) and (not re.search(r'米粉', summary)):
                        time.sleep(random.randint(8, 10))
                        headers = self.headers.copy()
                        headers["User-Agent"] = random.choice(UserAgent.fake_useragent())
                        print(summary)
                        # print(headers['User-Agent'])
                        logging.info(str(j) + f'--{url}')
                        res = requests.get(url, headers=headers, proxies={})
                        # {'https': '127.0.0.1:1080'}
                        self.base_msg(headers, res, meta)
            if not os.path.exists(fr'F:\农产品搜索指数\Baid_Spider\京东大米\基本信息2\{name}.csv'):
                data = []
                data.append(
                    {'商品名称': '', '商品店铺': '', '商品链接': '', '商品重量': '',
                     '商品价格': '', '商品视频': '', '优惠活动': '',
                     '京东物流': '',
                     '7天无理由': '', '企业品牌': '', '进出口': '',
                     '包装': '', '等级': '', '商品产地': '', '产品标准号': '',
                     '保质期': '', '绿色食品': '',
                     '地理标志产品': '', '有机产品': '', '溯源': '',
                     '全部评价': '', '好评度': '',
                     '晒图': '', '视频晒图': '', '好评': '', '中评': '',
                     '差评': ''})
                self.save_list(data, f'{name}.csv', data[0].keys())

    # 基本信息
    def base_msg(self, headers, response, meta):
        html = response.text
        res = etree.HTML(html)

        if '该商品已下' in html or '您访问的页面' in html:
            return
        skuId = re.findall('skuid: (.*?),', html)[0] if re.findall('skuid: (.*?),', html) else ''
        if skuId == '':
            return
        cat = re.findall('cat: \[(.*?)],', html)
        if cat == ['1320,1584,2675']:

            shopId = re.findall("shopId:'(.*?)',", html)[0]
            venderId = re.findall('venderId:(.*?),', html)[0]
            paramJson = re.findall("paramJson: '(.*?)' ,", html)[0]
            pid = re.findall("mainSkuId:'(.*?)'", html)[0]

            # 商品名称
            p_name = res.xpath('//div[@class="sku-name"]/text()')
            p_name = ''.join(p_name).replace('\n', '').replace('  ', '')

            p_lists = res.xpath('//ul[@class="parameter2 p-parameter-list"]//text()')
            p_lists = ''.join(p_lists).replace('  ', '')
            p_lists = p_lists.split('\n')

            # 视频
            p_video = '1' if 'shangpin|keycount|product|picvideo' in html else '0'

            p_dict = {}
            # 保质期
            p_listss = res.xpath('//div[@class="Ptable-item"]/dl/dl')
            for str1 in p_listss:
                name = str1.xpath('.//dt/text()')[0]
                value = str1.xpath('.//dd/text()')[0]
                p_dict[name] = value

            for one in p_lists:
                if one:
                    one = one.strip(' ').split('：')
                    p_dict[one[0]] = one[1]

            # 商品重量
            p_wight = p_dict.get('商品毛重', '')

            # 商品产地
            p_place = p_dict.get('商品产地', '')
            # 商品价格
            p_price = meta['price']

            # 品牌
            p_brand = res.xpath('//ul[@id="parameter-brand"]/li//text()')
            p_brand = ''.join(p_brand).replace('\n', '').replace(' ', '')

            # 保质期
            p_shelflife = p_dict.get('保质期', '')
            # 产品标准号
            p_standard = p_dict.get('产品标准号', '')
            # 是否进口
            p_import = p_dict.get('国产/进口', '')
            # 包装形式
            p_pack = p_dict.get('包装形式', '')
            # 等级
            p_level = p_dict.get('等级', '')

            # 判断是否有优惠券, 京东物流, 7天无理由
            # headers = self.headers.copy()
            headers['referer'] = 'https://item.jd.com/'
            # cat = '1320,1584,2675'
            area = ['2_2825_61086_0', '12_904_905_52655', '2_2825_51936_0', '2_2825_51934_0', '12_904_3376_57875',
                    '1_72_55653_0']
            params = {
                'callback': "jQuery" + str(int(1e7 * random.random())),
                'skuId': skuId,
                'cat': cat[0],
                # area 送货地址
                'area': random.choice(area),
                'shopId': shopId,
                'venderId': venderId,
                'paramJson': paramJson,
                'num': 1
            }
            meta_copy = dict(skuId=skuId, pid=pid, venderId=venderId, name=meta['name'], shop_name=meta['shop_name'],
                             url=meta['url'], p_name=p_name, p_wight=p_wight, p_price=p_price, p_standard=p_standard,
                             p_place=p_place, p_brand=p_brand, p_video=p_video,
                             p_import=p_import, p_pack=p_pack, p_level=p_level, p_shelflife=p_shelflife)
            print(params)
            time.sleep(0.2)
            response = requests.get(url='https://item-soa.jd.com/getWareBusiness', params=params, headers=headers,
                                    proxies={})
            self.is_coupons(headers, response, meta_copy)

    def is_coupons(self, headers, response, meta):
        html = response.text
        # 优惠活动
        coupons = re.findall('"discountText":"(.*?)",', html)[0] if re.findall('"discountText":"(.*?)",', html) else ''
        # 京东物流
        logistics = '1' if '京东物流为该商品提供预约送货服务' in html else '0'
        # 是否7天无理由
        is7toreturn = '0' if '不支持7天无理由退货' in html else '1'
        # 品质溯源
        p_roots = '1' if '品质溯源' in html else ''
        # 商品价格
        p_p_price = re.findall('"p":"(.*?)",', html)[0] if re.findall('"p":"(.*?)",', html) else ''

        # 地理标识，有机产品，是否可溯源
        # headers = self.headers.copy()
        headers['referer'] = 'https://item.jd.com/'
        params = {
            'callback': "jQuery" + str(int(1e7 * random.random())),
            'skuId': meta['skuId'],
            'pid': meta['pid'],
            'catId1': 1320,
            'catId2': 1584,
            'catId3': 2675,
            'venderId': meta['venderId'],
            '_': int(time.time() * 1000)
        }

        aaa = dict(coupons=coupons, logistics=logistics, is7toreturn=is7toreturn, p_roots=p_roots, p_p_price=p_p_price)
        meta.update(aaa.copy())
        meta_copy = deepcopy(meta)
        print(params)
        time.sleep(0.2)
        res = requests.get(url='https://cd.jd.com/qualification/life_v2', params=params, headers=headers, proxies={})
        self.mark(headers, res, meta_copy)

    def mark(self, headers, response, meta):
        html = response.text
        p_organic = '1' if '中国有机' in html else ''
        p_mark = '1' if '地理标志产品' in html else ''
        p_green = '1' if '绿色食品' in html else ''
        # 好评度

        # headers = self.headers.copy()
        headers['referer'] = 'https://item.jd.com/'
        params = {
            'callback': 'fetchJSON_comment98',
            'productId': meta['skuId'],
            'score': 0,
            'sortType': 6,
            'page': 0,
            'pageSize': 10,
            'isShadowSku': 0,
            'fold': 1,
        }
        aaa = dict(p_organic=p_organic, p_mark=p_mark, p_green=p_green)
        meta.update(aaa)
        meta_copy = deepcopy(meta)
        print(params)
        time.sleep(0.2)
        res = requests.get(url='https://club.jd.com/comment/skuProductPageComments.action', params=params,
                           headers=headers, proxies={})
        self.evaluation(res, headers, meta_copy)

    def evaluation(self, response, headers, meta):
        data = []
        html = response.text
        if html == '':
            params = {
                'callback': 'fetchJSON_comment98',
                'productId': meta['skuId'],
                'score': 0,
                'sortType': 5,
                'page': 0,
                'pageSize': 10,

                'isShadowSku': 0,
                'fold': 1,
            }
            chrome = [
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.2228.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.20 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.19 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.43 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.15 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.113 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.41 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.10 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.17 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.18 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.35 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.20 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.48 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.17 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.20 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            ]
            headers["User-Agent"] = random.choice(chrome)
            print('重新评价' + headers["User-Agent"])
            html = requests.get(url='https://club.jd.com/comment/skuProductPageComments.action', params=params,
                                headers=headers, proxies={}).text
        # 全部评价
        commentCountStr = re.findall('"commentCountStr":"(.*?)",', html)[0] if re.findall('"commentCountStr":"(.*?)",',
                                                                                          html) else ''
        # 好评度
        goodRate = re.findall('"goodRate":(.*?),', html)[0] if re.findall('"goodRate":(.*?),', html) else ''
        if commentCountStr == '0':
            goodRate = ''

        # 晒图
        imageListCount = re.findall('"imageListCount":(.*?),', html)[0] if re.findall('"imageListCount":(.*?),',
                                                                                      html) else ''
        # 视频晒图
        videoCountStr = re.findall('"videoCountStr":"(.*?)",', html)[0] if re.findall('"videoCountStr":"(.*?)",',
                                                                                      html) else ''
        # 好评
        goodCountStr = re.findall('"goodCountStr":"(.*?)",', html)[0] if re.findall('"goodCountStr":"(.*?)",',
                                                                                    html) else ''
        # 中评
        generalCountStr = re.findall('"generalCountStr":"(.*?)",', html)[0] if re.findall('"generalCountStr":"(.*?)",',
                                                                                          html) else ''
        # 差评
        poorCountStr = re.findall('"poorCountStr":"(.*?)",', html)[0] if re.findall('"poorCountStr":"(.*?)",',
                                                                                    html) else ''
        # data = item.CsvItem(data_storage=fr'F:\农产品搜索指数\Baid_Spider\京东大米\基本信息', filename=f'{meta["name"]}')
        data.append({'商品名称': meta['p_name'], '商品店铺': meta['shop_name'], '商品链接': meta['url'], '商品重量': meta['p_wight'],
                     '商品价格': meta['p_p_price'], '商品视频': meta['p_video'],
                     '优惠活动': meta['coupons'],
                     '京东物流': meta['logistics'],
                     '7天无理由': meta['is7toreturn'], '企业品牌': meta['p_brand'], '进出口': meta['p_import'],
                     '包装': meta['p_pack'], '等级': meta['p_level'], '商品产地': meta['p_place'], '产品标准号': meta['p_standard'],
                     '保质期': meta['p_shelflife'], '绿色食品': meta['p_green'],
                     '地理标志产品': meta['p_mark'], '有机产品': meta['p_organic'], '溯源': meta['p_roots'],
                     '全部评价': commentCountStr, '好评度': goodRate,
                     '晒图': imageListCount, '视频晒图': videoCountStr, '好评': goodCountStr, '中评': generalCountStr,
                     '差评': poorCountStr})

        print(data)
        self.save_list(data, f'{meta["name"]}.csv', data[0].keys())


if __name__ == '__main__':
    c = JdDetail()
    c.first_requests()

    """https://search.jd.com/search?keyword=%E5%B0%84%E9%98%B3&qrst=1&spm=2.1.0&stock=1&cid3=2675"""
    """https://search.jd.com/search?keyword=太子&wq=太子&cid3=2675"""
