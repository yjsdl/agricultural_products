# -*- coding: utf-8 -*-
# @Time    : 2022/11/07 14:11
# @Author  : crab-pc
# @File    : jd_search.py
import execjs
import re
from Yjsdl import Spider, item
from copy import deepcopy
import pandas as pd


def getpvid():
    with open('./pvid.js', 'r', encoding='utf-8') as f:
        file = f.read()

    context = execjs.compile(file)
    res = context.call('getpvid')
    return res


class JdSearch(Spider):
    request_config = {
        "RETRIES": 3,
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
    }
    advware_count = 0
    repeat_count = 0

    async def start_requests(self):
        pf = pd.read_csv(r'F:\农产品搜索指数\Baid_Spider\大米标识.csv', dtype=str)
        sha = pf.shape[0]
        for i in range(0, 1):
            pvid = getpvid()
            keyword = pf.values[i][1]
            keyword = '睢宁籼米'
            params = {
                'keyword': keyword,
                'enc': 'utf-8',
                'wq': keyword,
                'pvid': pvid
            }
            refer = f'https://search.jd.com/Search?keyword={keyword}&enc=utf-8&wq={keyword}&pvid={pvid}'
            headers = self.headers
            headers['referer'] = refer
            meta = dict(keyword=keyword, pvid=pvid, mi_name=keyword, refer=refer, page=1)
            yield self.request(
                url='https://search.jd.com/Search',
                params=params,
                headers=headers,
                meta=meta,
            )

    async def parse(self, response):
        meta = response.meta
        html = await response.text()

        res = response.html_etree(html=html)
        p_num = re.findall("result_count:'(.*?)',", html)[0]
        if '没有找到' in html:
            self.logger.info(f'没有找到{meta["keyword"]}')
            data2 = item.CsvItem(data_storage=r'F:\农产品搜索指数\Baid_Spider\spiders', filename='未找到大米数量')
            data2.append(dict(name=meta['mi_name'], num=0))
            yield data2

            data = item.CsvItem(data_storage=r'F:\农产品搜索指数\Baid_Spider\地理产品大米', filename=meta['mi_name'])
            data.append(dict(name='', link='', price='', summary=''))
            yield data

        else:
            # 获取商品信息
            shop_lists = res.xpath('//div[@class="gl-i-wrap"]')
            for one_shop in shop_lists:
                # 店铺名称
                name = one_shop.xpath('.//div[@class="p-shop"]/span/a/text()')
                # 店铺网址
                link = one_shop.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')
                # 商品价格
                price = one_shop.xpath('.//div[@class="p-price"]/strong/i/text()')
                # 商品摘要
                summary = one_shop.xpath('.//div[@class="p-name p-name-type-2"]/a/em//text()')

                summary = ''.join(summary).replace('\n', '')
                if name and '米' in summary:
                    name = name[0].replace('\n', '').replace(' ', '')
                    link = 'https:' + link[0].replace('\n', '').replace(' ', '')
                    price = ''.join(price)
                    data = item.CsvItem(data_storage=r'F:\农产品搜索指数\Baid_Spider\地理产品大米', filename=meta['keyword'])
                    data.append(dict(name=name, link=link, price=price, summary=summary))
                    yield data

            if int(p_num) > 30 and len(shop_lists) == 30:
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
                    'keyword': meta['keyword'],
                    'qrst': 1,
                    'wq': meta['keyword'],
                    'stock': 1,
                    'pvid': meta['pvid'],
                    'page': meta.get('page') + 1,
                    's': start,
                    'scrolling': 'y',
                    'log_id': log_id,
                    'tpl': '1_M',
                    'isList': 0,
                    'show_items': show_items
                }
                headers = self.headers
                headers['referer'] = meta['refer']
                yield self.request(
                    url='https://search.jd.com/s_new.php',
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
                    if int(page_count) > 8:
                        page_count = 8
                    meta['max_page'] = int(page_count) * 2
                    self.logger.info(f'{meta["keyword"]}找到{page_count}页商品')
                    # 统计数量
                    data1 = item.CsvItem(data_storage=r'F:\农产品搜索指数\Baid_Spider\spiders', filename='大米数量')
                    data1.append(dict(name=meta['keyword'], num=int(page_count)))
                    yield data1
                    # # 新的页面爬取
                    for page in range(3, meta['max_page']):
                        if self.advware_count > 0:
                            start = (page - 1) * 30 - self.advware_count + 1 + self.repeat_count
                        else:
                            start = (page - 1) * 30 + 1
                        if page % 2 != 0:
                            params = {
                                'keyword': meta['keyword'],
                                'qrst': 1,
                                'wq': meta['keyword'],
                                'stock': 1,
                                'pvid': meta['pvid'],
                                'page': page,
                                's': start,
                                'click': 0,
                            }
                            headers = self.headers
                            refer = f'https://search.jd.com/Search?keyword={meta["keyword"]}&qrst=1&wq={meta["keyword"]}&stock=1&pvid={meta["pvid"]}&page={page}&s={start}&click=0'
                            headers['referer'] = refer

                            meta_copy = dict(keyword=meta['keyword'], pvid=meta['pvid'], refer=refer, max_page=page_count, page=page)
                            yield self.request(
                                url='https://search.jd.com/s_new.php',
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
            link = one_shop.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')
            # 商品价格
            price = one_shop.xpath('.//div[@class="p-price"]/strong/i/text()')
            # 商品摘要
            summary = one_shop.xpath('.//div[@class="p-name p-name-type-2"]/a/em//text()')

            summary = ''.join(summary).replace('\n', '')
            if name and '米' in summary:
                name = name[0].replace('\n', '').replace(' ', '')
                link = 'https:' + link[0].replace('\n', '').replace(' ', '')
                price = ''.join(price)

                data = item.CsvItem(data_storage=r'F:\农产品搜索指数\Baid_Spider\地理产品大米', filename=meta['keyword'])
                data.append(dict(name=name, link=link, price=price, summary=summary))
                yield data


if __name__ == '__main__':
    JdSearch.start()
    # getpvid()