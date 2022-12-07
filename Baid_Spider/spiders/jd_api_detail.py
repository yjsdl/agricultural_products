# -*- coding: utf-8 -*-
# @Time    : 2022/11/17 09:12
# @Author  : crab-pc
# @File    : jd_api_detail.py
import pandas as pd
import time
import re
import random
import json
from copy import deepcopy
from Yjsdl import Spider, item


class JdApiDetail(Spider):
    request_config = {
        "RETRIES": 3,
        "DELAY": 1,
        "TIMEOUT": 20
    }
    # 并发
    concurrency = 1
    # aiohttp_kwargs = {'proxy': 'http://127.0.0.1:1080'}

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
    }

    async def start_requests(self):
        pf1 = pd.read_csv('F:\农产品搜索指数\Baid_Spider\地理标识.csv', dtype=str)
        sha1 = pf1.shape[0]
        for i in range(1, 2):
            name = pf1.values[i][1]
            logo = pf1.values[i][2]
            path = fr'F:\农产品搜索指数\Baid_Spider\地理产品大米\{name}.csv'
            pf = pd.read_csv(path, dtype=str)
            sha = pf.shape[0]
            for j in range(15, 20):
                # time.sleep(random.randint(8, 12))
                url = pf.values[j][1]
                shop_name = pf.values[j][0]
                price = pf.values[j][2]
                summary = pf.values[j][3]
                meta = dict(name=name, price=price, shop_name=shop_name, url=url)
                if logo in summary:
                    yield self.request(
                        url=url,
                        headers=self.headers,
                        meta=meta,
                        request_config={
                            "DELAY": 10,
                        }
                    )

    # 基本信息
    async def parse(self, response):
        meta = response.meta
        html = await response.text()
        res = response.html_etree(html=html)
        # 商品名称
        p_name = res.xpath('//div[@class="sku-name"]/text()')
        p_name = ''.join(p_name).replace('\n', '').replace('  ', '')
        # 商品重量
        p_lists = res.xpath('//ul[@class="parameter2 p-parameter-list"]//text()')
        p_lists = ''.join(p_lists).replace('  ', '')
        p_lists = p_lists.split('\n')
        p_dict = {}
        for one in p_lists:
            if one:
                one = one.strip(' ').split('：')
                p_dict[one[0]] = one[1]
        p_wight = p_dict.get('商品毛重', '')

        # 商品价格
        p_price = meta['price']

        # 品牌
        p_brand = res.xpath('//ul[@id="parameter-brand"]/li//text()')
        p_brand = ''.join(p_brand).replace('\n', '').replace(' ', '')

        # 是否进口
        p_import = p_dict.get('国产/进口', '')
        # 包装形式
        p_pack = p_dict.get('包装形式', '')
        # 等级
        p_level = p_dict.get('等级', '')

        skuId = re.findall('skuid: (.*?),', html)[0]
        cat = re.findall('cat: \[(.*?)],', html)[0]
        shopId = re.findall("shopId:'(.*?)',", html)[0]
        venderId = re.findall('venderId:(.*?),', html)[0]
        paramJson = re.findall("paramJson: '(.*?)' ,", html)[0]
        if cat == '1320,1584,2675':
            # 判断是否有优惠券, 京东物流, 7天无理由
            headers = self.headers.copy()
            headers['referer'] = 'https://item.jd.com/'
            # cat = '1320,1584,2675'
            params = {
                'callback': "jQuery" + str(int(1e7 * random.random())),
                'skuId': skuId,
                'cat': cat,
                'area': '12_904_905_52655',
                'shopId': shopId,
                'venderId': venderId,
                'paramJson': paramJson,
                'num': 1
            }
            meta_copy = dict(skuId=skuId, venderId=venderId, name=meta['name'], shop_name=meta['shop_name'],
                             url=meta['url'], p_name=p_name, p_wight=p_wight, p_price=p_price, p_brand=p_brand,
                             p_import=p_import, p_pack=p_pack, p_level=p_level)
            yield self.request(
                url='https://item-soa.jd.com/getWareBusiness',
                params=params,
                headers=headers,
                meta=meta_copy,
                callback=self.is_coupons
            )

    async def is_coupons(self, response):
        meta = response.meta
        html = await response.text()

        # 优惠活动
        coupons = re.findall('"discountText":"(.*?)",', html)[0] if '优惠券' in html else ''
        # 京东物流
        logistics = '1' if '京东物流为该商品提供预约送货服务' in html else '0'
        # 是否7天无理由
        is7toreturn = '0' if '不支持7天无理由退货' in html else '1'
        # 品质溯源
        p_roots = '1' if '品质溯源' in html else ''

        # 地理标识，有机产品，是否可溯源
        headers = self.headers.copy()
        headers['referer'] = 'https://item.jd.com/'
        params = {
            'callback': "jQuery" + str(int(1e7 * random.random())),
            'skuId': meta['skuId'],
            'pid': meta['skuId'],
            'catId1': 1320,
            'catId2': 1584,
            'catId3': 2675,
            'venderId': meta['venderId'],
            '_': int(time.time() * 1000)
        }

        aaa = dict(coupons=coupons, logistics=logistics, is7toreturn=is7toreturn, p_roots=p_roots)
        meta.update(aaa.copy())
        meta_copy = deepcopy(meta)
        yield self.request(
            url='https://cd.jd.com/qualification/life_v2',
            params=params,
            headers=headers,
            meta=meta_copy,
            callback=self.mark
        )

    # 地理标志
    async def mark(self, response):
        meta = response.meta
        html = await response.text()
        p_organic = '1' if '中国有机' in html else ''
        p_mark = '1' if '地理标志产品' in html else ''
        # 好评度

        headers = self.headers.copy()
        headers['referer'] = 'https://item.jd.com/'
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
        aaa = dict(p_organic=p_organic, p_mark=p_mark)
        meta.update(aaa)
        meta_copy = deepcopy(meta)
        yield self.request(
            url='https://club.jd.com/comment/skuProductPageComments.action',
            params=params,
            meta=meta_copy,
            headers=headers,
            callback=self.evaluation,
        )

    # 评价
    async def evaluation(self, response):
        meta = response.meta
        html = await response.text()
        print(html)
        # 全部评价
        commentCountStr = re.findall('"commentCountStr":"(.*?)",', html)[0] if re.findall('"commentCountStr":"(.*?)",',
                                                                                          html) else ''
        # 好评度
        goodRate = re.findall('"goodRate":(.*?),', html)[0] if re.findall('"goodRate":(.*?),', html) else ''
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
        data = item.CsvItem(data_storage=fr'F:\农产品搜索指数\Baid_Spider\京东大米\基本信息', filename=f'{meta["name"]}')
        data.append({'商品名称': meta['p_name'], '商品店铺': meta['shop_name'], '商品链接': meta['url'], '商品重量': meta['p_wight'],
                     '商品价格': meta['p_price'], '优惠活动': meta['coupons'],
                     '京东物流': meta['logistics'],
                     '7天无理由': meta['is7toreturn'], '企业品牌': meta['p_brand'], '进出口': meta['p_import'],
                     '包装': meta['p_pack'], '等级': meta['p_level'],
                     '地理标志产品': meta['p_mark'], '有机产品': meta['p_organic'], '溯源': meta['p_roots'],
                     '全部评价': commentCountStr, '好评度': goodRate,
                     '晒图': imageListCount, '视频晒图': videoCountStr, '好评': goodCountStr, '中评': generalCountStr,
                     '差评': poorCountStr})
        yield data


if __name__ == '__main__':
    JdApiDetail.start()
