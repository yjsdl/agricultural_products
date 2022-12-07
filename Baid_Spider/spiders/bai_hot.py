# -*- coding: utf-8 -*-
# @Time    : 2022/10/27 15:33
# @Author  : crab-pc
# @File    : bai_hot.py
import time
import re
import pandas as pd
from Yjsdl import Spider, item
from urllib.parse import quote


class BaiHot(Spider):
    request_config = {
        "RETRIES": 1,
        "DELAY": 0,
        "TIMEOUT": 20
    }
    # 并发
    concurrency = 1
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'BD_UPN=12314753; MSA_WH=360_740; PSTM=1656579001; BIDUPSID=68950CB420629398BE9A724207EAB2DD; MCITY=-%3A; BAIDUID=82E90F9E4A52AC66697A0D35FB930844:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; bdindexid=euq02kq5h6va46thcuc9nrn5e4; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04168603955R1pProxXACYvu%2F59Ioq%2Bo1eGxfEUvqFD%2BxXorOP7Wrhf0n7iOFE79gowBRCgBT6qKztzj5Avh4G9LuD5AGMs2ek%2FRjxsYF6fiahVrAnPdh5%2FmVr9db9muuV6pIkd5WcJ4UFqXWmvO6YspJLONVzIU3jn8nv5ytLDbEWdA2RcIeLxQrgCFy%2F%2F3lvogU1chrm%2BFcfiva0oFdf5%2B9gnamUzfJV3I4CPTXmFL1OSKeAhKV6VzCBzV6SsnYFIsuvGdMKuuGDVFaRHnaqcIYYnv37jKSrI6Vjz1mFYdJ20EqRT5Vs%3D07270236687812735151729059859830; BDUSS=Ud1Uk1PREVvb2ZNZ2l6T3dzYk9FbExuVkZUMkdMOTFZN1plSXcxZXVXMjlwNEZqSUFBQUFBJCQAAAAAAAAAAAEAAAAM2QdeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0aWmO9GlpjW; BDSFRCVID=k98OJexroG0leprjSmw7Jdh1GopWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJIJ_ID2JCD3H48k-4QEbbQH-UnLq-owtgOZ04n-ah02fJoVj46p3xLQyxO3Jxb-W20jbUjm3UTKsq76Wh35K5tTQP6rLttOb6c4KKJxbpbG8J5IytKaQMu3hUJiBMAHBan7Wx7IXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM5fT02-CLKKJ03bk82J-_Hn7zen7PLU4pbq7H2M-jbGQW_Jc73p7iORbdDfJqyUnQbPnn0pcr3GTKWRjYtqjlhxLm34JK3fDkQN3T-pRPHCj4LT6FfncbDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfJAfoCK2tIP3H48k-4QEbbQH-UnLq5oA22OZ04n-ah02qlbz-P6oX40D5PuqtnbLW20j0h7m3UTdsq76Wh35K5tTQP6rLtbHQmr4KKJxbU7lKJ6H5Kcke-IWhUJiBMPHBan70pOIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM-l-X5to05TIX3b7Ef-bWhh7_bJ7KhUbQK4OL5-TyLI6jLhIKJP3VOpkxbUnxQhFTQtnfXpOe-n7rKhc1QJ3KSqoHQT3m5h4Aqfc4-IrZfIQfWb3cWhkK8UbSbMbPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGLsa46b56-X3JjV5PK_Hn7zeP4BeM4pbq7H2M-jaITjQJcRa40bORbdDfJoKh-bWHon0pcH3mJT0JTq2R6US4Kz3x6qLTKkQN3T-ntDHCn4L66NWPbfDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KChJCKBhU5; ab_sr=1.0.1_M2M5ZDZlMWEzYjJlNzZiYjAwZTMzYjE1ZjliZmFmNzY4OWYyMWY0Njk2MTdmN2Q2MDYwNmQ3ODExODg2MzUzN2UxZjI4YzgxOGYzZDdlOTQ0NWY1OWQxNmMwYjEyNTE3NTFhODdmNzk1ODg5OGMzM2E2Yzc2ZmZhZmExMzg2OTE1Mzk5MjRiMmQ4YmU1MWNjMTZmYzQwNTljYzI4OWY0Yg==; BDUSS_BFESS=Ud1Uk1PREVvb2ZNZ2l6T3dzYk9FbExuVkZUMkdMOTFZN1plSXcxZXVXMjlwNEZqSUFBQUFBJCQAAAAAAAAAAAEAAAAM2QdeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0aWmO9GlpjW; H_PS_PSSID=36549_37636_37517_37584_36884_34812_37627_36803_36789_37532_37500_26350_37454; BAIDUID_BFESS=82E90F9E4A52AC66697A0D35FB930844:SL=0:NR=10:FG=1; BDSFRCVID_BFESS=k98OJexroG0leprjSmw7Jdh1GopWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJIJ_ID2JCD3H48k-4QEbbQH-UnLq-owtgOZ04n-ah02fJoVj46p3xLQyxO3Jxb-W20jbUjm3UTKsq76Wh35K5tTQP6rLttOb6c4KKJxbpbG8J5IytKaQMu3hUJiBMAHBan7Wx7IXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM5fT02-CLKKJ03bk82J-_Hn7zen7PLU4pbq7H2M-jbGQW_Jc73p7iORbdDfJqyUnQbPnn0pcr3GTKWRjYtqjlhxLm34JK3fDkQN3T-pRPHCj4LT6FfncbDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfJAfoCK2tIP3H48k-4QEbbQH-UnLq5oA22OZ04n-ah02qlbz-P6oX40D5PuqtnbLW20j0h7m3UTdsq76Wh35K5tTQP6rLtbHQmr4KKJxbU7lKJ6H5Kcke-IWhUJiBMPHBan70pOIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM-l-X5to05TIX3b7Ef-bWhh7_bJ7KhUbQK4OL5-TyLI6jLhIKJP3VOpkxbUnxQhFTQtnfXpOe-n7rKhc1QJ3KSqoHQT3m5h4Aqfc4-IrZfIQfWb3cWhkK8UbSbMbPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGLsa46b56-X3JjV5PK_Hn7zeP4BeM4pbq7H2M-jaITjQJcRa40bORbdDfJoKh-bWHon0pcH3mJT0JTq2R6US4Kz3x6qLTKkQN3T-ntDHCn4L66NWPbfDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KChJCKBhU5; delPer=0; BD_CK_SAM=1; PSINO=5; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=2848bVOtx6Fg0n3YaNlwX13WCdE69vEndR%2BxDsBzXt%2FHEtdb2XRoow8nihI; BA_HECTOR=0k8k25ak0l21ah800k8k1uqc1hlkgi21a; ZFY=BdiWXbmGxreJhGzopSe27v9WpGjH5Q0ie:B7dI8ML6FI:C; baikeVisitId=1a916680-3784-4ec4-9864-dac1f7c86c5d; B64_BOT=1; BAIDUID=ADB97949CE80F44AC682FB98332B9A3F:FG=1; BIDUPSID=ADB97949CE80F44AFD56A5378445DBB2; H_PS_PSSID=36549_37636_37517_37584_36884_34812_37627_36803_36789_37532_37500_26350_37454; PSINO=5; PSTM=1647502543; delPer=0; BDSVRTM=458; BD_CK_SAM=1',
        'Pragma': 'no-cache',
        'Referer': 'https://www.baidu.com/s?wd=%E9%BB%8E%E5%9F%8E%E6%A0%B8%E6%A1%83&rsv_spt=1&rsv_iqid=0xaaf2a073002f51ee&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&rsv_dl=tb&rsv_btype=i&inputT=5864&rsv_t=5331VXIdrB5zdGYzy5Mk51y3NcumAItGT7WMEXcCz2ie1mqkbduIBNNo%2B3651dLlPfaZ&gpc=stf%3D1609430400%2C1640880000%7Cstftype%3D2&tfflag=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'is_pbs': '%E9%BB%8E%E5%9F%8E%E6%A0%B8%E6%A1%83',
        'is_referer': 'https://www.baidu.com/s?wd=%E9%BB%8E%E5%9F%8E%E6%A0%B8%E6%A1%83&rsv_spt=1&rsv_iqid=0xaaf2a073002f51ee&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=0&rsv_dl=tb&rsv_sug3=5&rsv_n=2&rsv_sug1=1&rsv_sug7=100&rsv_btype=i&prefixsug=%25E9%25BB%258E%25E5%259F%258E%25E6%25A0%25B8%25E6%25A1%2583&rsp=4&inputT=5864&rsv_sug4=7194',
        'is_xhr': '1',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    async def start_requests(self):

        pf = pd.read_csv('../农产品.csv', dtype=str)
        sha = pf.shape[0]
        for i in range(0, 2):
            name = pf.values[i][2]
            year = '2011'
            start_year = f'{year}-01-01'
            end_year = f'{year}-12-31'

            timeArray_stat = time.strptime(start_year, "%Y-%m-%d")  # 把起始时间解析成时间元组
            timeArray_end = time.strptime(end_year, "%Y-%m-%d")  # 把结束时间解析成时间元组
            start = str(int(time.mktime(timeArray_stat)))  # 把起始时间改成时间戳
            end = str(int(time.mktime(timeArray_end)))

            params = {
                'wd': name,
                'gpc': f'stf={start},{end}|stftype=2',
                'tfflag': 1
            }
            meta = dict(name=name, year=year)
            yield self.request(
                url='https://www.baidu.com/s',
                params=params,
                headers=self.headers,
                meta=meta
            )

    async def parse(self, response):
        meta = response.meta
        html = await response.text()
        obj = re.compile(r'<span class="hint_PIwZX c_font_2AD7M">百度为您找到相关结果(.*?)个</span>', re.S)
        try:
            hot_num = int(obj.findall(html)[0].replace(',', '').replace('约', ''))
        except:
            hot_num = 0

        self.logger.info(f'{meta["name"]}的{meta["year"]}的指数为{str(hot_num)}')
        data = item.CsvItem(data_storage=f'../百度热度', filename=f'{meta["year"]}')
        data.append({'name': meta['name'], f'{meta["year"]}': hot_num})
        yield data


if __name__ == '__main__':
    BaiHot.start()
    # import re
    # import requests
    #
    # # 获取指定时间段内关键词百度热度函数（2021-01-01：2021-12-31）
    # def get_hot_num(keyword, start, end):
    #     # 百度搜索界面请求头
    #     headers = {
    #         'Accept': '*/*',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Cache-Control': 'no-cache',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'BD_UPN=12314753; MSA_WH=360_740; PSTM=1656579001; BIDUPSID=68950CB420629398BE9A724207EAB2DD; MCITY=-%3A; BAIDUID=82E90F9E4A52AC66697A0D35FB930844:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; bdindexid=euq02kq5h6va46thcuc9nrn5e4; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04168603955R1pProxXACYvu%2F59Ioq%2Bo1eGxfEUvqFD%2BxXorOP7Wrhf0n7iOFE79gowBRCgBT6qKztzj5Avh4G9LuD5AGMs2ek%2FRjxsYF6fiahVrAnPdh5%2FmVr9db9muuV6pIkd5WcJ4UFqXWmvO6YspJLONVzIU3jn8nv5ytLDbEWdA2RcIeLxQrgCFy%2F%2F3lvogU1chrm%2BFcfiva0oFdf5%2B9gnamUzfJV3I4CPTXmFL1OSKeAhKV6VzCBzV6SsnYFIsuvGdMKuuGDVFaRHnaqcIYYnv37jKSrI6Vjz1mFYdJ20EqRT5Vs%3D07270236687812735151729059859830; BDUSS=Ud1Uk1PREVvb2ZNZ2l6T3dzYk9FbExuVkZUMkdMOTFZN1plSXcxZXVXMjlwNEZqSUFBQUFBJCQAAAAAAAAAAAEAAAAM2QdeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0aWmO9GlpjW; BDSFRCVID=k98OJexroG0leprjSmw7Jdh1GopWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJIJ_ID2JCD3H48k-4QEbbQH-UnLq-owtgOZ04n-ah02fJoVj46p3xLQyxO3Jxb-W20jbUjm3UTKsq76Wh35K5tTQP6rLttOb6c4KKJxbpbG8J5IytKaQMu3hUJiBMAHBan7Wx7IXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM5fT02-CLKKJ03bk82J-_Hn7zen7PLU4pbq7H2M-jbGQW_Jc73p7iORbdDfJqyUnQbPnn0pcr3GTKWRjYtqjlhxLm34JK3fDkQN3T-pRPHCj4LT6FfncbDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfJAfoCK2tIP3H48k-4QEbbQH-UnLq5oA22OZ04n-ah02qlbz-P6oX40D5PuqtnbLW20j0h7m3UTdsq76Wh35K5tTQP6rLtbHQmr4KKJxbU7lKJ6H5Kcke-IWhUJiBMPHBan70pOIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM-l-X5to05TIX3b7Ef-bWhh7_bJ7KhUbQK4OL5-TyLI6jLhIKJP3VOpkxbUnxQhFTQtnfXpOe-n7rKhc1QJ3KSqoHQT3m5h4Aqfc4-IrZfIQfWb3cWhkK8UbSbMbPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGLsa46b56-X3JjV5PK_Hn7zeP4BeM4pbq7H2M-jaITjQJcRa40bORbdDfJoKh-bWHon0pcH3mJT0JTq2R6US4Kz3x6qLTKkQN3T-ntDHCn4L66NWPbfDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KChJCKBhU5; ab_sr=1.0.1_M2M5ZDZlMWEzYjJlNzZiYjAwZTMzYjE1ZjliZmFmNzY4OWYyMWY0Njk2MTdmN2Q2MDYwNmQ3ODExODg2MzUzN2UxZjI4YzgxOGYzZDdlOTQ0NWY1OWQxNmMwYjEyNTE3NTFhODdmNzk1ODg5OGMzM2E2Yzc2ZmZhZmExMzg2OTE1Mzk5MjRiMmQ4YmU1MWNjMTZmYzQwNTljYzI4OWY0Yg==; BDUSS_BFESS=Ud1Uk1PREVvb2ZNZ2l6T3dzYk9FbExuVkZUMkdMOTFZN1plSXcxZXVXMjlwNEZqSUFBQUFBJCQAAAAAAAAAAAEAAAAM2QdeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0aWmO9GlpjW; H_PS_PSSID=36549_37636_37517_37584_36884_34812_37627_36803_36789_37532_37500_26350_37454; BAIDUID_BFESS=82E90F9E4A52AC66697A0D35FB930844:SL=0:NR=10:FG=1; BDSFRCVID_BFESS=k98OJexroG0leprjSmw7Jdh1GopWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJIJ_ID2JCD3H48k-4QEbbQH-UnLq-owtgOZ04n-ah02fJoVj46p3xLQyxO3Jxb-W20jbUjm3UTKsq76Wh35K5tTQP6rLttOb6c4KKJxbpbG8J5IytKaQMu3hUJiBMAHBan7Wx7IXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM5fT02-CLKKJ03bk82J-_Hn7zen7PLU4pbq7H2M-jbGQW_Jc73p7iORbdDfJqyUnQbPnn0pcr3GTKWRjYtqjlhxLm34JK3fDkQN3T-pRPHCj4LT6FfncbDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfJAfoCK2tIP3H48k-4QEbbQH-UnLq5oA22OZ04n-ah02qlbz-P6oX40D5PuqtnbLW20j0h7m3UTdsq76Wh35K5tTQP6rLtbHQmr4KKJxbU7lKJ6H5Kcke-IWhUJiBMPHBan70pOIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC86Dj_MD5vM-l-X5to05TIX3b7Ef-bWhh7_bJ7KhUbQK4OL5-TyLI6jLhIKJP3VOpkxbUnxQhFTQtnfXpOe-n7rKhc1QJ3KSqoHQT3m5h4Aqfc4-IrZfIQfWb3cWhkK8UbSbMbPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGLsa46b56-X3JjV5PK_Hn7zeP4BeM4pbq7H2M-jaITjQJcRa40bORbdDfJoKh-bWHon0pcH3mJT0JTq2R6US4Kz3x6qLTKkQN3T-ntDHCn4L66NWPbfDn3oyUkKXp0nhJnly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KChJCKBhU5; delPer=0; BD_CK_SAM=1; PSINO=5; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=2848bVOtx6Fg0n3YaNlwX13WCdE69vEndR%2BxDsBzXt%2FHEtdb2XRoow8nihI; BA_HECTOR=0k8k25ak0l21ah800k8k1uqc1hlkgi21a; ZFY=BdiWXbmGxreJhGzopSe27v9WpGjH5Q0ie:B7dI8ML6FI:C; baikeVisitId=1a916680-3784-4ec4-9864-dac1f7c86c5d; B64_BOT=1; BAIDUID=ADB97949CE80F44AC682FB98332B9A3F:FG=1; BIDUPSID=ADB97949CE80F44AFD56A5378445DBB2; H_PS_PSSID=36549_37636_37517_37584_36884_34812_37627_36803_36789_37532_37500_26350_37454; PSINO=5; PSTM=1647502543; delPer=0; BDSVRTM=458; BD_CK_SAM=1',
    #         'Pragma': 'no-cache',
    #         'Referer': 'https://www.baidu.com/s?wd=%E9%BB%8E%E5%9F%8E%E6%A0%B8%E6%A1%83&rsv_spt=1&rsv_iqid=0xaaf2a073002f51ee&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&rsv_dl=tb&rsv_btype=i&inputT=5864&rsv_t=5331VXIdrB5zdGYzy5Mk51y3NcumAItGT7WMEXcCz2ie1mqkbduIBNNo%2B3651dLlPfaZ&gpc=stf%3D1609430400%2C1640880000%7Cstftype%3D2&tfflag=1',
    #         'Sec-Fetch-Dest': 'empty',
    #         'Sec-Fetch-Mode': 'cors',
    #         'Sec-Fetch-Site': 'same-origin',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    #         'X-Requested-With': 'XMLHttpRequest',
    #         'is_pbs': '%E9%BB%8E%E5%9F%8E%E6%A0%B8%E6%A1%83',
    #         'is_referer': 'https://www.baidu.com/s?wd=%E9%BB%8E%E5%9F%8E%E6%A0%B8%E6%A1%83&rsv_spt=1&rsv_iqid=0xaaf2a073002f51ee&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=0&rsv_dl=tb&rsv_sug3=5&rsv_n=2&rsv_sug1=1&rsv_sug7=100&rsv_btype=i&prefixsug=%25E9%25BB%258E%25E5%259F%258E%25E6%25A0%25B8%25E6%25A1%2583&rsp=4&inputT=5864&rsv_sug4=7194',
    #         'is_xhr': '1',
    #         'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-ch-ua-platform': '"Windows"'
    #     }
    #     # 查找关键词热度的正则式
    #     obj = re.compile(r'<span class="hint_PIwZX c_font_2AD7M">百度为您找到相关结果(.*?)个</span>', re.S)
    #     # 请求关键词搜索页面
    #     resp = requests.get(
    #         'https://www.baidu.com/s?wd=' + keyword + '&gpc=stf%3D' + start + '%2C' + end + '%7Cstftype%3D2&tfflag=1',
    #         headers=headers)
    #     resp.encoding = 'utf-8'
    #     # 获取关键词热度值
    #     hot_num = int(obj.findall(resp.text)[0].replace(',', '').replace('约', ''))
    #     return hot_num
    #
    #
    # keyword = '黎城核桃'
    # year = '2011'
    # start_year = f'{year}-01-01'
    # end_year = f'{year}-12-31'
    #
    # timeArray_stat = time.strptime(start_year, "%Y-%m-%d")  # 把起始时间解析成时间元组
    # timeArray_end = time.strptime(end_year, "%Y-%m-%d")  # 把结束时间解析成时间元组
    # start = str(int(time.mktime(timeArray_stat)))  # 把起始时间改成时间戳
    # end = str(int(time.mktime(timeArray_end)))
    # # get_hot_num(keyword, start, end)

