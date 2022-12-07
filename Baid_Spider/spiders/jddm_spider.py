# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 09:20
# @Author  : crab-pc
# @File    : jddm_spider.py

import re
from copy import deepcopy
from Yjsdl import Spider, item


class JddmSpider(Spider):
    request_config = {
        "RETRIES": 2,
        "DELAY": 4,
        "TIMEOUT": 20
    }
    # 并发
    concurrency = 1

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'cookie': '__jdv=76161171|direct|-|none|-|1668577225160; __jdu=1668577225159618803337; areaId=12; PCSYCityID=CN_320000_320100_0; shshshfp=8b6f7c2d0b51f8986806d9d12e053c9c; shshshfpa=3606d9ef-6816-1ead-5c86-1bc19d087480-1668577226; shshshfpb=y4opCKEnhpwxQ2eOzwpe0cQ; jsavif=1; __jda=122270672.1668577225159618803337.1668577225.1668577225.1668577225.1; __jdc=122270672; token=273a039cf9c688826b54ea92a33d4510,2,926987; __tk=KVX0CcM6JiTZBVnwKVkdRtXpJi9fCVnwK1uiucMartRYutbbKqR2KaXuntRYRcfw4buPjvMN,2,926987; ip_cityCode=904; ipLoc-djd=12-904-907-50559; avif=1; jsavif=1; wlfstk_smdl=0dgw3f732j15qr8nsxpgx7ffx3tyd9jd; __jdb=122270672.15.1668577225159618803337|1.1668577225; shshshsID=a7623af75511d23677f0fcc71aa4256f_6_1668577358726; 3AB9D23F7A4B3C9B=U46XHD2SXKVHEAULFLBWK3NZRIIR6GS3WPOGNYWWJLJFAAZDK4BSKEO4EFS2DOBBRLJHYWF5WTDOZSINTE5CEVDFKE',
    }

    advware_count = 0
    repeat_count = 0

    async def start_requests(self):
        ev = '2682_3942^'
        cat = '1320,1584,2675'
        params = {
            'cat': cat,
            'ev': ev,
            'cid3': 2675
        }
        refer = f'https://list.jd.com/list.html?cat={cat}&ev={ev}&cid3=2675'
        meta = dict(cat='1320,1584,2675', refer=refer, page=1, ev=ev)
        headers = self.headers.copy()
        headers['referer'] = 'https://list.jd.com/list.html?cat=1320,1584,2675'
        yield self.request(
            url="https://list.jd.com/list.html",
            params=params,
            headers=headers,
            meta=meta,
        )

    async def parse(self, response):
        meta = response.meta
        html = await response.text()

        res = response.html_etree(html=html)
        # 获取商品信息
        shop_lists = res.xpath('//div[@class="gl-i-wrap"]')
        for one_shop in shop_lists:
            # 店铺名称
            name = one_shop.xpath('.//div[@class="p-shop"]/span/a/text()')
            # 店铺网址
            link = one_shop.xpath('.//div[@class="p-name p-name-type-3"]/a/@href')
            # 商品价格
            price = one_shop.xpath('.//div[@class="p-price"]/strong/i/text()')
            # 商品摘要
            summary = one_shop.xpath('.//div[@class="p-name p-name-type-3"]/a/em//text()')

            summary = ''.join(summary).replace('\n', '')
            if name and '米' in summary:
                name = name[0].replace('\n', '').replace(' ', '')
                link = 'https:' + link[0].replace('\n', '').replace(' ', '')
                price = ''.join(price)
                data = item.CsvItem(data_storage=r'F:\农产品搜索指数\Baid_Spider\京东大米', filename='普通大米')
                data.append(dict(name=name, link=link, price=price, summary=summary))
                yield data

        # 获取计算数量
        if meta.get('page', 1) == 1:
            count_list = re.findall('s.init\((.*?)\);', html)[0]
            count_list = count_list.split(',')
            self.advware_count = int(count_list[8])
            self.repeat_count = int(count_list[10])

        if self.advware_count > 0:
            start = meta.get('page') * 30 - self.advware_count + 1 + self.repeat_count
        else:
            start = meta.get('page') * 30 + 1
        # 获取当前页后30条数据
        log_id = re.findall('log_id:\'(.*?)\',', html)[0]
        show_items = re.findall('search000014_log:\{wids:\'(.*?)\',uuid', html)[0]

        params = {
            'cat': meta['cat'],
            'ev': meta['ev'],
            'page': meta.get('page') + 1,
            's': start,
            'scrolling': 'y',
            'log_id': log_id,
            'tpl': '1_M',
            'isList': 1,
            'show_items': show_items
        }
        headers = self.headers.copy()
        headers['referer'] = meta['refer']
        yield self.request(
            url='https://list.jd.com/listNew.php',
            params=params,
            headers=headers,
            priority=meta['page'],
            meta=deepcopy(meta),
            callback=self.detail_parse
        )

        # 获取后面页
        if not meta.get('max_page', ''):
            # 最大页数
            page_count = res.xpath('//div[@id="J_topPage"]/span/i/text()')[0]
            meta['max_page'] = int(page_count) * 2
            self.logger.info(f'{meta["ev"]}找到{page_count}页商品')
            # # 新的页面爬取
            for page in range(3, meta['max_page']):
                if self.advware_count > 0:
                    start = (page - 1) * 30 - self.advware_count + 1 + self.repeat_count
                else:
                    start = (page - 1) * 30 + 1
                if page % 2 != 0:
                    params = {
                        'cat': meta['cat'],
                        'ev': meta['ev'],
                        'page': page,
                        's': start,
                        'click': 0,
                    }
                    headers = self.headers.copy()
                    refer = f'https://list.jd.com/list.html?cat={meta["cat"]}&ev={meta["ev"]}&page={page}&s={start}&click=0'
                    headers['referer'] = refer

                    meta_copy = dict(cat=meta['cat'], ev=meta['ev'], refer=refer, max_page=page_count,
                                     page=page)
                    yield self.request(
                        url='https://list.jd.com/listNew.php',
                        params=params,
                        headers=headers,
                        priority=page,
                        meta=meta_copy,
                        callback=self.parse
                    )

        # 商品详情页信息

    async def detail_parse(self, response):
        meta = response.meta
        html = await response.text()
        res = response.html_etree(html=html)
        shop_lists = res.xpath('//div[@class="gl-i-wrap"]')
        for one_shop in shop_lists:
            # 店铺名称
            name = one_shop.xpath('.//div[@class="p-shop"]/span/a/text()')
            # 店铺网址
            link = one_shop.xpath('.//div[@class="p-name p-name-type-3"]/a/@href')
            # 商品价格
            price = one_shop.xpath('.//div[@class="p-price"]/strong/i/text()')
            # 商品摘要
            summary = one_shop.xpath('.//div[@class="p-name p-name-type-3"]/a/em//text()')

            summary = ''.join(summary).replace('\n', '')
            if name and '米' in summary:
                name = name[0].replace('\n', '').replace(' ', '')
                link = 'https:' + link[0].replace('\n', '').replace(' ', '')
                price = ''.join(price)

                data = item.CsvItem(data_storage=r'F:\农产品搜索指数\Baid_Spider\京东大米', filename='普通大米')
                data.append(dict(name=name, link=link, price=price, summary=summary))
                yield data


if __name__ == '__main__':
    JddmSpider.start()
