# -*- coding: utf-8 -*-
# @Time    : 2022/10/27 14:01
# @Author  : crab-pc
# @File    : bai__hot.py
import json
import pandas as pd
from Yjsdl import Spider, item


class BaiZS(Spider):
    request_config = {
        "RETRIES": 3,
        "DELAY": 0,
        "TIMEOUT": 20
    }
    # 并发
    concurrency = 1

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cipher-Text': '1666767759988_1666851157048_XGqQqpdyJBsXDBz5GELmvZvCI3vEpR61CEOumrCRpAzufWD2KW2WvhO4lb5hUregwQPhXXgxSBrFHUT2G+GBwdDnO5d3mbMwgcrVZsQqi02DwVNusjvQqBoVeLCQtASak5tu4/UJbxxWhjaYps53GAL7O60Qb/tPWFUcxZKbUxpOJuHdqgGu+XLCSjStQ6IN7UUPcH91zP26adu5F+2xxshXtILvl3h4iurSj+7pI8Eg9ct2+v0SWF5SVsENqZae3WUv6HtMReYMF4HXNylYvTaC6ax9mo5nc06CuQoD3xCJ7qjNbr/jKf4GzpQsfHSu4tJhTbV2E0xONULi2eFZqiMVtCXBsbTev4d8ntoY7yaloy1MSi2LNcpKJ8sbFYTh2XExwry+SnAl3ybubX0YBwlSFyChHaizYwA/wlW2lbDYaV8HTXw5ruX5T9cd+q0oGARtSiZcXNIcvrFTOHTm+0rzFUA1VbbQfBdVhD6OwnA=',
        'Connection': 'keep-alive',
        'Cookie': 'PSTM=1656579001; BIDUPSID=68950CB420629398BE9A724207EAB2DD; MCITY=-%3A; BAIDUID=82E90F9E4A52AC66697A0D35FB930844:SL=0:NR=10:FG=1; Hm_up_d101ea4d2a5c67dab98251f0b5de24dc=%7B%22uid_%22%3A%7B%22value%22%3A%221577572620%22%2C%22scope%22%3A1%7D%7D; BDUSS=Ud1Uk1PREVvb2ZNZ2l6T3dzYk9FbExuVkZUMkdMOTFZN1plSXcxZXVXMjlwNEZqSUFBQUFBJCQAAAAAAAAAAAEAAAAM2QdeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0aWmO9GlpjW; BAIDUID_BFESS=82E90F9E4A52AC66697A0D35FB930844:SL=0:NR=10:FG=1; ZFY=blvHFUh701YHP0pS0xLmEUtkk0Us9eWoRKdIvJvTn:B4:C; delPer=0; BA_HECTOR=0h8g212h85agaha10480c4lb1hluaok1a; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PSINO=5; H_PS_PSSID=36549_37517_37584_36884_34812_37627_36803_37662_36789_37532_37500_37670_26350_37454; BCLID=11253011636305075200; BCLID_BFESS=11253011636305075200; BDSFRCVID=vD0OJexroG0leprjDhruMMgFPcpWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=vD0OJexroG0leprjDhruMMgFPcpWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvhDRTvhCcjh-FSMgTBKI62aKDsXpQnBhcqJ-ovQT3hW4nBMRnRWhvZ5I-DKb5cWKJJ8UbeWfvp3t_D-tuH3lLHQJnp0-oG0q5nhMJmBp_VhfL3qtCOaJby523i2IovQpnV_pQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DTbLjH8jqTna--oa3RTeb6rjDnCrDfrOXUI82h5y05OH3Ij2BJ7k5n6bODLm5PcvyT8sXnORXx74B5vvbPOMthRnOlRKbn5lLxL1Db3JyhLLamTJslFy2t3oepvoyT5c3MkOLPjdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEtbkD_C-MfIvDqTrP-trf5DCShUFs-nkjB2Q-XPoO3KJKsb6nM4nm-J8WyHDJ--riWbRM2MbgylRp8P3y0bb2DUA1y4vpKbjP0eTxoUJ2XMKVDq5mqfCWMR-ebPRiB5j9Qgbb5hQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hDvYh4Oq2KCV-frb-C62aKDsBKIyBhcqJ-ovQT3SbJ8XMRbL-5bZ5I-DKb7MQ-nZMfbeWJ5pXh8EMfQ02x3pb4jpaJ5nJq5nhMJmKTLVbML0qto7-P3y523i2IovQpnV_pQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DjPthxO-hI6aKC5bL6rJabC3fl-xXU6q2bDeQN3QKROH2en3Qt5zBR3PVbOx3n7Zjq0vWq54WpOh2C60WlbCb664OR5JjxonDh83KNLLKUQtHmT7LnbO5hvv8KoO3M7VBUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRIJoK0K3e; H_BDCLCKID_SF_BFESS=tbkD_C-MfIvhDRTvhCcjh-FSMgTBKI62aKDsXpQnBhcqJ-ovQT3hW4nBMRnRWhvZ5I-DKb5cWKJJ8UbeWfvp3t_D-tuH3lLHQJnp0-oG0q5nhMJmBp_VhfL3qtCOaJby523i2IovQpnV_pQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DTbLjH8jqTna--oa3RTeb6rjDnCrDfrOXUI82h5y05OH3Ij2BJ7k5n6bODLm5PcvyT8sXnORXx74B5vvbPOMthRnOlRKbn5lLxL1Db3JyhLLamTJslFy2t3oepvoyT5c3MkOLPjdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEtbkD_C-MfIvDqTrP-trf5DCShUFs-nkjB2Q-XPoO3KJKsb6nM4nm-J8WyHDJ--riWbRM2MbgylRp8P3y0bb2DUA1y4vpKbjP0eTxoUJ2XMKVDq5mqfCWMR-ebPRiB5j9Qgbb5hQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hDvYh4Oq2KCV-frb-C62aKDsBKIyBhcqJ-ovQT3SbJ8XMRbL-5bZ5I-DKb7MQ-nZMfbeWJ5pXh8EMfQ02x3pb4jpaJ5nJq5nhMJmKTLVbML0qto7-P3y523i2IovQpnV_pQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DjPthxO-hI6aKC5bL6rJabC3fl-xXU6q2bDeQN3QKROH2en3Qt5zBR3PVbOx3n7Zjq0vWq54WpOh2C60WlbCb664OR5JjxonDh83KNLLKUQtHmT7LnbO5hvv8KoO3M7VBUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRIJoK0K3e; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1666847945,1667264619; bdindexid=42c2npe6e53980pvqpk15d7qe3; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04172770666DP3x9hXdfTrjrYu%2FjO%2FRdcGlf%2B%2FxYUDdXdYwnNoL%2BmIsHZyBQ46DXKvA7x3EGidw%2FocH9pKzsOVX1OOtJSJChPP9gku6Cn%2BU%2B63KvGGG4TinO9ryV6EthwFa%2Fmltn6UafP%2BCzz47beK4qf6IL0eXqlh9nM4rn333eYWiCPO4FeBLiwbNmbRLSkatJPee0Au%2BFinAYw3uykGbADl%2FOXzz6lVpw4iExXFs%2B0S0pWNyFiHVScdyDAUH%2Bu4N3ncgjZyyhbIZmJTKXKPTOMQ%2FMadThC2bkDFuaDUKZhd2qKwULs8%3D97516963622042518886391994619464; __cas__rn__=417277066; __cas__st__212=000a4aab7640e0ac362e44e1083926425b6bc48b7eeeebbcab26c710a6ce48087707cd3fbcfe518bc6dd4c8e; __cas__id__212=43331363; CPID_212=43331363; CPTK_212=639659434; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1667264854; ab_sr=1.0.1_MmQ1YzMwMmNlNDg5ODliOGU5ZmE1MzRiNWExMjA1YmFiNThhNTg4MTNmODYxZTE2NjI4MzA4NDExMWM2ZTViYjExZmFjNDI0ZTc0ZjE3NGQ2ZjFiYWVjOGY1YjVjOWI5YjVkYmQ0Njk0ZDU5YWJiMDVjY2ZjNmU2OTU3ZWE4MzdlNjFiODMyN2I3MzhiZjIzNjk3NDlmYzVmODMwNjUxMQ==; BDUSS_BFESS=Ud1Uk1PREVvb2ZNZ2l6T3dzYk9FbExuVkZUMkdMOTFZN1plSXcxZXVXMjlwNEZqSUFBQUFBJCQAAAAAAAAAAAEAAAAM2QdeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0aWmO9GlpjW; RT="z=1&dm=baidu.com&si=7a214ee6-9bd2-41a8-8b3f-3b0646ceed85&ss=l9xib0wq&sl=h&tt=9jm&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=6gtr"',
        'Pragma': 'no-cache',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    async def start_requests(self):
        pf = pd.read_csv('../农产品.csv', dtype=str)
        sha = pf.shape[0]
        for i in range(0, 1):
            name = pf.values[i][2]
            name = '阳澄湖大闸蟹'
            word = [[{"name": name, "wordType": 1}]]
            year = 2021
            params = {
                'area': 0,
                'word': json.dumps(word, ensure_ascii=True),
                'startDate': f'{year}-01-01',
                'endDate': f'{year}-12-31'
            }
            meta = dict(name=name, year=year)
            yield self.request(
                url='https://index.baidu.com/api/SearchApi/index',
                params=params,
                headers=self.headers,
                meta=meta
            )

    async def parse(self, response):
        meta = response.meta
        text = await response.text()
        html = await response.json()
        try:
            # 获取平均值相关数据
            data_avg = html['data']['generalRatio'][0]
            # 获取日均值数据
            data_avg_all = data_avg['all']['avg']
        except:
            data_avg_all = 0
        self.logger.info(f'{meta["name"]}的{meta["year"]}的指数为{str(data_avg_all)}')
        data = item.CsvItem(data_storage=f'../百度指数', filename=f'{meta["year"]}')
        data.append({'name': meta['name'], f'{meta["year"]}': data_avg_all})
        yield data


if __name__ == '__main__':
    BaiZS.start()
