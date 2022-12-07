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
from Crypto.Cipher import AES
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
browser = webdriver.Chrome(executable_path=r'D:\python38\chromedriver.exe',
                           options=chrome_options)  # executable执行webdriver驱动的文件


# 保存到csv文件
def save_list(data, file, name):
    # desk = os.path.join(os.path.expanduser('~'), 'Desktop')
    # 当前文件夹
    file_path = r'F:\农产品搜索指数\Baid_Spider\抖音指数\\' + file
    if os.path.isfile(file_path):
        df = pd.DataFrame(data=data)
        df.to_csv(file_path, encoding="utf-8", mode='a', header=False, index=False)
    else:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df = pd.DataFrame(data=data, columns=name)
        df.to_csv(file_path, encoding="utf-8", index=False)

# 定义Browser类：获取signature接口签名
# class Browser():
#     def __init__(self):
#         chrome_options = Options()      # 创建options对象
#         chrome_options.add_argument('--headless')  # 无头模式
#         chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
#         chrome_options.add_argument('log-level=2')  # 日志级别
#
#         self.browser = webdriver.Chrome(service=Service(r"D:\python38\chromedriver"), options=chrome_options)     # 打开chromedriver
#         self.browser.get('https://trendinsight.oceanengine.com/arithmetic-index')       # 打开巨量抖音算数指数网址

    """
    获取接口签名的方法
    """

def signature(keyword, start_date, end_date):
    # 运行script
    sign_url = browser.execute_script('''
                function queryData(url) {
                   var p = new Promise(function(resolve,reject) {
                       var e={"url":"https://trendinsight.oceanengine.com/api/open/index/get_multi_keyword_hot_trend",
                                "method":"POST",
                                "data" : '{"keyword_list": ["%s"],"start_date": "%s","end_date": "%s","app_name": "aweme"}'};
                        var h = new XMLHttpRequest;h.open(e.method, e.url, true);
                        h.setRequestHeader("accept","application/json, text/plain, */*");  
                        h.setRequestHeader("content-type","application/json");
                        h.onreadystatechange =function() {
                             if(h.readyState != 4) return;
                             if(h.readyState === 4 && h.status  ===200) {
                                resolve(h.responseURL);
                             } else {
                              }
                        };
                        h.send(e.data);
                        });
                        return p;
                    }
                var p1 = queryData('fc');
                res = Promise.all([p1]).then(function(result){
                return result
                })
                return res;
    ''' % (keyword, start_date, end_date))
    return sign_url[0]  # 返回数据所在链接地址
    #
    # def close(self):
    #     self.browser.close()
    #     self.browser.quit()



# 获得指定时间段内抖音搜索指数相关数据（2021-01-01：2021-12-31）
def get_data(keyword, start_date, end_date):
    # 请求头文件
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': 'MONITOR_WEB_ID=15f71935-fe57-45a6-be0a-35cdc498dd7a; x-jupiter-uuid=16668618983981848; Hm_lvt_c36ebf0e0753eda09586ef4fb80ea125=1666861899; passport_csrf_token=88dedcf7fb1e5c47b88415caae2b005b; passport_csrf_token_default=88dedcf7fb1e5c47b88415caae2b005b; Hm_lpvt_c36ebf0e0753eda09586ef4fb80ea125=1666929950; msToken=kTbEwNwr_WcCLYSlvdHA78l7Tu8RmvSyXYoqPwIwb0fam3fB3GjMBdKYCY1xKYv-ipvHBIxalZzNgrO9l23wYqslCkMVWUQVHVF5y1oc3XJes1KDKh_vq3xtRwsSVLE=; tt_scid=Dly94N9OxMkVv0QZfadPkRtKezFZUYw9PSEy0eAurG8OZzTKNjr1X8IRAAcA4ijGc266; _csrf_token=U_03eNDn-siAoByPlKD4dB09',
        'origin': 'https://trendinsight.oceanengine.com',
        'pragma': 'no-cache',
        'referer': f'https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword={quote(keyword)}&appName=aweme',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    # 请求data数据
    # data = '{"keyword_list": ["%s"],"start_date": "%s","end_date": "%s","app_name": "aweme"}' % (
    #     keyword, start_date, end_date)
    data = {
        'keyword_list': json.dumps([f'{keyword}'], ensure_ascii=True),
        'start_date': start_date,
        'end_date': end_date,
        "region": '[]',
        'app_name': 'aweme'
    }
    # 获取数据所在网址链接
    sign_url = signature(keyword=keyword, start_date=start_date, end_date=end_date)
    print(sign_url)
    # 请求页面响应
    resp = requests.post(sign_url, headers=headers, data=data, proxies={})
    # resp = requests.post(sign_url, headers=headers, data=data)
    print(resp.text)
    doc = resp.json()['data']       # 获取json中data字段
    return doc      # 返回加密数据


# AES-128 解密
def decrypt(_str):
    iv = "amlheW91LHFpYW53".encode(encoding='utf-8')
    key = 'anN2bXA2NjYsamlh'.encode(encoding='utf-8')
    cryptor = AES.new(key=key, mode=AES.MODE_CFB, IV=iv, segment_size=128)
    decode = base64.b64decode(_str)
    plain_text = cryptor.decrypt(decode)
    _plain_text = str(plain_text, encoding='utf-8')
    # 查找抖音搜索指数的正则式
    obj = re.compile(r'"average":{"average":".*?","search_average":"(.*?)"}', re.S)
    # 查找抖音搜索指数数据
    aver_data = obj.findall(_plain_text)[0]

    print(name, aver_data)
    return aver_data        # 返回抖音日搜索平均值


if __name__ == '__main__':
    pf = pd.read_csv('../农产品.csv', dtype=str)
    sha = pf.shape[0]
    year = '2021'
    start_date = f'{year}-01-01'   # 起始时间
    end_date = f'{year}-12-31'     # 结束时间

    for i in range(997, 1000):
        data = []
        name = pf.values[i][2]
        # browser = Browser()     # 创建Browser对象
        # 获取2021-01-01至2021-12-31时间段内抖音搜索指数日均值
        try:
            # datas = get_data(name, start_date.replace('-', ''), end_date.replace('-', ''))
            datas = {"data":"cRnz6pNXHJMIyQ4SZSlKSfSqi76CVtwyfSwfJ0aSj1UVYZL8wbgZxX5Kmo2sBZnLO1UHVP6LL36f8FdiMQayxLtct3f3FQ27kePftn7fLnX2BQioESLOwqfXN5251eBvH/rHYW0O4BFSn9ML55hbulLsNROCbMwowpuJFZa+sNoJsEpNYLqhDoCv2VnUkdVJtDxnOG+ccRQeJKZ99lbxUDYvxdbZgn8BME6G2k+ypVqf0BeDT1xcxdcoarerfnwjvIfqMLxW0cOFBkU9czFQVdiLwzlVkMcJtC+IEuPz/BBKUyynYPEj2o8EqSTQjpWOhHKfVZWfHCYkEc5QGrv6vmNugdOF71bblUPxPCIlW3ZxMIDjOVTJ/W5yH20MMt4KCSEFg4YcVLLJKugZ0Y5H6KcfdtC4vWxiPFVwohbe9yR6UfzK1Qz1vSVblHDa4i1YPuEkOG/A75GHTJ6NEQPiEgmmVWUvoRpLazd3InX2122h8Qt6wCcvsgYELB+bUXLfuQZ2ipLHvtPK0Qg8TPzSZy7sb8DZ2ff46k0d0OK9yBgX2PKQaGiRgjSETMTZqa4xl/4Iubb61MQ44L4Xzw9LeffiCHrx3s1TbJnhksF0pirMvzr8NVyM0j98eI2HMWzDcK7z+T/f8dgvjlQFNKRRm75ILriTflfLYUgT0vqZHm1avP1zd6TTT296E0uGOUbkvNXdnHY/mOtMZ2fxayw13Zr/+qFkWINQmUV8tB+GZSkFPy1JZNA7rSp8V+PgEQPGs0O/jU2cbqzqooqHHo03jCWNTupqJZVaCm/zIpEgvZ7KCqGM+/TayUSg/aes6Hz6U42M83ZjjNMf+YfpyLNJyPuh/UmGWOCnQtcJKLTKDW3uuwUX02oDFjMeNZoj1ZNiEt5Nnm5zjpSL7O0mVSLwSm263UYfwFX0j+3+wlZSmSDqiL8n8RTbFI71c3bdf+gciSt6mAl46rSzTrVJowO3nYNhqOTcUt4sNHUUQdM41z77W5G2pYR6ZxSYwZ/QwHK3xFqyLpSX1/zXE6lme0q89L4k26qzYyxxBjjcmSNP7n8G2P38BhljpDK3g8Id5C7rogz8TIf6If0aqJhr+acLDDZJS3WHUtnASZJg3ScJS6qA0hoNPNkqbupLJQH9IdP523uKS+2aQG7eQQYYpZUjiY7eOoPiHubrWGGp/cSxVP2hWU1GPZYryZhqnYTtgY66Icoqw7nBMWJAUCPv+fHU5cx8/mKNyGBTf98zciwCScIa5vrzxCntGzo3Svdccn5nVjmgkQY2OqgqSVGhsFIja8jbRjRj5dCwHN0X5PXaHoIky7niklR9cRJS7pwYMFviWUL7Lj8YuWsCf+nHlHyEDWHNmGB65Lav2955ZJhFktDs+2c3MQCg3hGwYnk18/x8KBud0W5pp0w7Oxak3LfKJ+ktkkJpvs041ZI6MAyHZVnIqTfgrCCQ/N/PgkJhKFZQDbil3zKqamWhD+PnL3z1EAwXY5LDCcVbmw675M63kITgW/2Zo1hiLHYDVLPdAcXwy9R4o1QtvvdyeSJ7G73exYyR4uQF6h05MHqXtd3AJFC8TVTqPyFRQOwxOOLG3YQ8dZMy2spIACJ68io4ag0+Hjkk5YpCcUZ7CGRBkXoB/hcI79fCG6pNuMpzwgKB0aqXFjEhxjTyf9+K7yrjllDLXn3P3TtV5rNSxnuG2Ug7Xjf9I6VJMtB2DwvKHPXko8BwyR+ftpYa3/MZHhKGsgCR03GRvdDxpZ5nTb0nLH06obtiOE0x7X+1iQr7HonCFM19JiXXFMptxXjfqc8i7BCaLmZga5Ch3qGNrziFRMVAvByIGtRHIRSKFgwPTlGQViCN7r7fi6MxnleFyhKJy+hz4NyedEJstTws2ZilcTHnVo8HnVYjmI9eZ+F0nb2xvP+QRpNS3FEsW+Cwt7m4zrNyBrVF5N3G2avbF9whkQKiTETw/j7gpqlKxtXn9bSRoT61hJAuqEqK4QVU0JXckHpOsfGXwsUyaEbU1j8x3e+zC1dDoDjUZiQcGKQ+7a/7qZEyIynFzSYBzFuu1zT1yGeW5hoTXus3vfI/OQ2EYfBlOWx/gJTDdT8HUUCD39aiYlYsOjWjDUz/syVWm7Tb2GYWLOFm+kGkXImoEVWWfxgfwxPloOqW6AymKINoDRVQ8DihWnIxcGzZ6eKsg03YXwy1jJAH15XeI/3IYL5YTyRJtGVyStmz8+yEtymN+0qDj9wMD24u04bLog117tGaIzWEWUCmWKqS++EBLIGwgk7oELFzS6ESrDyQvsR4QUJ5XOEdofsFjaGqwKFgpP5X2H3OlcRtjRKUT9w3uK6WlYRBeOvsU2H7dyttPrV4H0rYmBbslLU48cz+n/W+n4/4qzdufwDpjBtYQssEyzCzGPi2A4jZjjPH/sVHI2gSOF0NWimk+cOexCH/Kmq8G1MP3PLguqmW3EexWWUY96Z/7/tSOtMmfDjqwohGZZEupD4sdAnrJNjPR5/dmcz6bfdyx4/mwQY4Xx4yKWSdASp9h+8IjfVzc7tKBNp33eQhBkxJuyEcljUWw2ivJDi4fSk5LLpMivSRwrzArvrqrfRaRW3BqNdFA4FdrcOrpFsdFD8ZV78NTA29lSWrXErahSP7hqnGpZ+6R1mwjLVBhsxc6pnxCIcE5hNtNQxcTWtYn5ZuskdVgzyyDwKjh343f3vmV1+8bcXC7FagitwBRv/p2b8GC2EZNCBRshNCyDu1auDi8Cw8r6H0R7EldwViliCv07ro8qQylWIfmvYVjnn26Bk+ra2IBdyS9/wYCGHFC4/5O2eA2sI3f9dm6SYw8pAizXahKwYufpV4XcoekJE7DvAej2xn/j5CPNBiIcmSa8YrmRqJD7qcpIvxBeDUYqlZ7Cm0POvvrYQ4b12hAWeZA0ygM92AkLWWw5vg47Z1VxT4ViQbpKyIB63dzbbzLNkTwB5iWbuLItvK0WwFtkc+iZ//nv1pfxysK6rftMCWEJy/ZtTA7UGa50mEsSai6dA9W+mf5ilQNg+BaGAoXNimZB8FElr9BCbdKFcIeKyr/mPct1a0QUc1bmbUbGfe6gPDqF70jzemUSXzH1QMs6sOnmjye+4xNNTy90rSUbgJOIZmnApIJA6WMTTaTqLvCzOfNysiqu5kwGUYkqX0woHh7eBhoPjW/iX6mY2tZrhrTmQiEZjzK6sLs0cRTkfkK4K7DpbjvMFqRfnIheaO/5bwM2lPqAN3Ha1woqxE+D8iG7KXrOqAlcqZMtXL807YzjM7DAGoU4ZEqqXfn/2U2gLblinp0MITkqH187/5nf/R5ZO5+PYjA+JKqgKDf1B+jwdecwJaYFf8CViXajoFQ8zweq8c7pMxvZZuUTQ1MvThUxEgNWshb6rWgYv4ish/9GJioICLUeJUT2ZptJSsvXkxahOV8WFCnIKxKquJq7ZRmYDWEwKAf5DFX6bMCcyDtwKECxNOp2ZA3LkekZXlErhMHKKWwsBcpIMzIOL7GWsn5fgoSqHjXqbkG2SDmik5zoQxaVK82DlXHATIlSwcN6KHN39EQEKs+mt/9rv4BAxXK0+P8W/T9XasrLjsn3v1g5V328qv25j87aUV6thqt/Kp92ymjgrhys9kGVHazA9peqLGYkSEupsziDyODWXAlIzVUn8R+AdKxHKqF9cKN8zf+pN4lTK5sp0XJDbicmnDJhAVNwQYp7/42hT/Qo+UQ64kPtSUDkaicaiORM3dmWL1oTZ08ssP2wgKnkSGk/xG+C74RrpbKbzsmflLihJ1bNUqZa7ZIZN++YmgwzaAaU6j517+7ofzXQ96UA4xsrQ1hobEfwejMpanZetcwjlJLH6vxZIUOf0BAdV/QsMpjPX67YyRSFqr2bf5D68PrxwJuUfngM3ok2Nqiu9pUDGIgK+65ekFQGvxdjuTQZbYEoRtqODd6+amWFXCCO+HO3pATBlpHO5/3hy995jTRa3UO6lzeLCtiLvl98/0sdW9Kll5fqh/WKuXgYeYnIGbDl9WzBMsLN59fbpHXAFodp4FVaGocu8xT7+PSoIB8kresrENb8GTffcnKNLtQ/AshAj5MT233+Gci605lFL3Iz+jM5bDNlcpdlBW/Bijyz/cg183AlS8x0KQXb4/Cxa6kG2VB//fHSRhWf0qIs3z4hiHUUiFIR9kpM6uNoj78jhQYotevEqxu7XAQXotNOTIruDHZRQ4nZFl/rCBDQVP0itqYQCmovrReeJ5Kii0pm3sh4hURv+otltZCArycnhucFOnP60D4FnOSKxBDG4kDrVjH19twPm684hSjX2pEhVWDQoThOtbcXE9A86Ua+dXSNquArcoz61pV0HKQX7SRUeXllwxtz1eYLZhRya9t+EaZERA2ijY0bAKCx9/RJKPZZiPwNbq521aQdoGXZO1QKdhdFkiw+2JpAnrr9Vbug/Qv4LMdSq+Y6uJy9yl0cq0SiruEAnhYZuv9LSiGzGuq/GnvTVAksMUW7ABIGbyHjjF5wrbKzg0QYInrCkaUTPY4oMxhFIbuCw46unvsqZ8LJrAgRg1BHIhj/YwxTdKdiZaE72p9iuh8sjBUqV+e3tVoD7Px8H1eYLvn1UMmu9YaFCVPDpL+mMXtFpKhhEfqQ4IcOvCXEIHJcCAQ/8hl1Iqs7E+24kDBSvZMW5jHDReROrai42KdVAO5HViLtQj0afEoS00a3B1fW7QIfTR8sMWQf/MUlkB4v5pFnq7jPJ4oMiSYg9wR9yDJWiQvyc/pB3VudjaZ8HorlPQHd8kgMrzjY2iPpRKbRV9kdDcI5sewlBtSDjiYomtJi0zVOAWSZ4LwLXEQFpsqapvKoernxWNuHY7fMqhTYzjJ3nAx2CxrxAnvUz+0VvUT8E4jYREWVLPaRsdR66rlaomJEFxi8T7UYvAYeXM2Hs+Sx7ABmSSHuyBaz8XUd9Rm7y5k9zEVar5/Tc8GSBqMVe6u2sMrC3zZDQl5sGB4USZECVD+qarnz3ZyRoU58RPp967xc+gR1KmS150RbFwwWfdpE2+c9+r7tuNOJK8cz3XnzP2FaiTkolhqtXuGAtQAU6OIvNvE1k4U8LdgH/lIIo1swm8yH3kdK10J3RBfDrbS/9tlYBf4PDB3L2hcqNo7SDb+UAnTzjtX4K6mabtcV5Cwig4VbmjMRHUY6Dmu99QH7gIh06fq4CwOKODO+/CvxYs93iw//uNEGuvOUAqNNViqH8ygNZ5tORoxrULf8itP13+TyYUN/VLrWo4Dhwo0RhP3dP1kKPwSwGDH4zmiMBpU59hD2YarNztYSGDneNoSmaoVOfqIpufeIzwsKVgWDlwIojfM5AIYlfQqFgO580RFyOzM1SL3z9lmWCc+JbeuDGLuhKNf4VRKNZClplue4NlQ/PDzMkYnwMfyaW7R5s/MvvUE9QMgWB0/Ok8FeMmlbH8LBdj0vxAyjQYDklV+sXele8eSzqJvWnZ0s28lCq8qWVqIYfTb95DEj5xXllYUVwecNY65hh1Xf7GgfpCAs3o5gKvr48n295GU2XGEzlfHZdN8jlRlZnnyoC2oxOaa0dXUIi1yM82M4D3Ryu+wpi1Q4mSJXKHrgZbh3N4wyEJ0igywppZyY+6mgsExWPG0J1ruvNfG6+owf+SIhlX3hMwYgl7Psb3H64VGPIzgH47uyT0iP1ZDf1zpB7+8zM0Db+0gf+5LKKMrwr7veRU+7RcCDtL2aZxOv0zmd351XJ4jrTysmtAeHBgfajYYcsUWhKxaN5H+QeAZGSe80mQRn3lokauwZzdlKUeCOBx6CUaR4e++lS9j/2TF6rMvHB0YwjIb9mc9mcBWEUpih59/XWz081Fv2Y++FdKGZvlo9j1t1WYZqkaQqg9jL63fv+YlWHEYGMeFC6w+WSfeirWS5iQ17d+f0cHrEfouuGetLDYEWDxbw5XmLAIsrghE/HM/EvWtguIxkt5WAO5E15drs0E/DBAp8jeqWiaEm8oY3B2qzieWyVSBQcphHI7OCykHM7ngk18QrUK9WjIf+Dj+Ty8UVMLgoHAiygW7JzoJ7uaWWelKgSqje9SRgey7hRPZ8DnH/3NEfeozrEaIgXLURTOSUM0LYJMa8HdD0WSLHZODgids2GoKAN7aFKY5TLwHgqchI1v8N8jpQ251Wgg6Iq2YOYI4oz1gYk78qK2US7V0XuGPDXckqLQ3vYns3qdYITQl/80D1NTXg1F4gz0uRzeHji/m1VnMN6dxIe3hZXpUA+xfhDXl/x/RCtOAvap4ejUtDXWwnL2G5+flMo9rW0lSCpkry0mGSsGLVt1CpUGrG51wn1hImto6O5Jqk0MUmkZldKkYjOhzsv63M3GlMKbTB0Hpu6Lsm11MKA3pxtTYhvnVSH+O4pwn6eXksZzUeSBmYs1EK3QRL0rVyg/tX9fYOU8tP9CrTBIFa+dJhXsRTDKmgbiMHJWqLUItiXk5aremzvDBgLjxXB8vvPyyUFvebOjFrIDa28FchpXsh23GYYay6oMXUeg6Z4J8bRrYPborMGv6XjVIfLfUlWzNGGzDrb04T+qULd/8KYTeH991vIKu0R9s8PNj+o+PV/qA0Pp+HDK69ac4g3Pcg+r9qlviS0/3F+FJak0QszE2XsbpMOftbC5lFm1myHglRwHFodsuusKglUQp7hqwOY73kU3Znxt5qj05UvQTBxjJzQIn65P3xS+00AKNRC7aItqIK0fMRSeV3u9e598t+KdDWVzCggWRQDWn97M6b4042Ecw5L9bmzTu0hu0/fGTSRCqdQwHYZ58V/L2tfzG/iPdXN3A+XFXK9pk+c/ummTdk01KDVGsQZxUGpDPmk7QTn7agEr4iYUHDx6f33E3P5XgJqEX9zLMjPKJf6FRvmkefabpR7u/zLIMA89qMyd9ZE5CBlHndIHJBOgwXIZu9e7N+OviHzSBZN/XPiNCZlim8k/SURPXfypyRyAo80pDHL/+I/PCWe5NE0+htarSvr0MB6VV+sR9eKsr+9IlcJI2wqc1U1ZsfG7G81GGi3RVNQSADEvAroIWtJ4T12QbBP+dE9Jq8w9hkZkvS8fjfb4GW2Kd30O83TD78hUDjmD/TdfbEqaajR9etF5ulIaAs7dfcOIE4D2jGaIoNSFGFVH+DbxEq/vxZQ2kU3JlhzGM0T/QAUgur9zZNjJdEpMtDmSBUkUEtzvQ3DRG4JBEasRfFFhroYHLolTZii9IThpwwmCuTPffDskPbgMNxdalHJEnN5+W6sqcJ2SR1XJJS7701P0f+dRej/GUhi4E8OBFJuL1zmXwnSc+Hwp1EXNhUcvHKlqck29eTKzVZG2qVNiYEkkq6ooYmcsa0Tp0noNf2NsL4Zht4++7UaQMREYBou5hhU1hGvxLbkkdoOiVzfm/Tq094uXPjDbijNpMk8SGgXoWEaekTGWvJrfETaEPWluBG4eOk26PahDd46oXldJVmilj7ZRHKlTkTSYijbviNeRgMEhcIjb3+FPyZl/qkVYg9A01Y0D8Esp5lrxo6aQAlRzwiPa6/aUxtdLiDF02ES6RFltaOb71M3rcmaw8lwLwKsb696yX7cKoOZiBzI/942WRnvVfNPbXnCFhcYKDCxkrR/kcCm8WvYZBrSeq5aTjawbUiigFPDet+Y3Z/5+REMDOtdFBY1XdauD4xsjxRVPCx3c641gChQe0lFZ+UZMuT8HKxpqFwqE1drhfpxjf6JuQutQXpBDdjoYWgmwbi3cgIJzokpejtIb3iS9e+6AVPHJ5W7DX3aFJjVfLRYLIEUjtUsTrFMVGsY7SEEX+KXuDviP7Xjeed/fVfhhvg0dThTtfPuy/APJbD27q803hRv+9DUTwgoLEWMxprFr7jTZAvu2Gu8l3ADTr1OSRs98a5Hya6AO/5i4BjTCzhSJLN86E1CjeXN2MTMHxekX1iWKcx+VIINTyBsi1fGvC9/FYqvHDoe1hhNiimmZOaZ9ZY/9oW+MmqydbubRoVwnstI5UycpKcF6UJzAW1KW7Bw/trYGK1SXXLBnxCCS1ScWIq0fFXpL7gbjke5eCdPxHoADJ2h/BJ673G0GFKC9lYoOJSll0Egi8QAXqKNqk9gOguu7SCdX4m/fa11ZlmI7qm+8AFRe0XtqOuW0iG2fEOnYWPsFwYijTHmNUCchsFQ28cSaPfoxmieKfLIt0g7lJCLN53ARn+g+IxnhDv7ELLIFlYO1gSMBZneXL1mAvlYEeGzYshenaa/PJgL/z05Kuob0CzJED/tsl+zF9v4DtNGTqBbu5thK5EFLfixy+GauqH/n2lFh5LSTkD/SBU237rsWxSJmBjPk/fSIDvXy19nFaORenvJO7ZffdD0B9pRvGoOTt0zJ2NE0Go7ucOEsAtFCduYBhQTf3kxsu/m2nt29RAprh+YU5fYUWBbUVoKS18tPHMqQx6CTdeeoXVTt73qELG99Xsng2+JFlTqOpDt0dNOWKP/teNonqCDZ13urLopRAC/MGLkl4wNOKStliLGmuArZR+LGNmgfJvWc8asrjS9/JJfMG9wEb23h3auRA7vbw6qgO9Iq15oh1lL7AjTwVtERFqzwIdcCoTPdHXiGOpD05AB7ULO7oiW67A8yubY4mT0kiv9M1IBTiXN7Kz1xU52MPdmK0lLLH3F//oLwfd7g72/xK4sGxZM1UMkJhBjfGQnCX9Iaolvo6w0AqyHkpkUrBv1T4IbdPf8MzPbuRWvY9baKIa8LYN4n5RUKuujAIdVxrTOkgYWeiGVBJ5tXB8bP3oCjDQLizJV3XHQI+aHyZoNnkiH2MSee8smrYRHY1qU/iOv1CIdf/NDJHjl0QcMCLd/YjuQ/RciTNSW7yfc95ya6M6mHAxf0BdxPOKulcPC1P6ib0bMS3dSTXphx7sR2w1iynKkB+Sox3nA3BHczxbYab5OEmmC4ti+hxaKjB+xGGFmifIBhka10cbn3PahMFYXzK/Wm2O1t1cqoafCCBFBk9pmWWJHHC/XFtrcqp4gSY8Ix1CziTJLUg2uyGApGbUJiMX+NpMJ7UAmccALT4i38Ho7+ekxOqfnWEEM+MfFkU/a8NXsbmeFrV2HLBmr6Hw+QNa0DQckrJQloeI/l6rkeAUSdA4PnvOc8DnZabDl5uFFGhpQQz+Uojaba3BP31jA0zpd5JrsdGxNF/AZWeo7LbgRrXCAMaIY4oD0AceBJkunBU9QvW8o+QbJQMX4CKdl0QKOKZETl9QSKIm+yEPcS/3EUFU+MMAe0rvftmlf1JoniMGfj2RNj2g2vS1oXZsdGJu3EpCu9uboqy2TJSURL8E3fm+E+i2A0fzujt7gQtBh3Mvg4R+DP+SVtWVjIy7M+34fqGD4vf8kdDUbll1m6BfvNdZOWEjxoA2fcen3pm9VfdwFxiiHTRfkU5zsvKYu3UWWFLIKxjNdDmCbYvAuQUnupcUJV3SiNmw8bnZk1UpkpsRFzUu23PQD3fOHfxbfQOAs+XVxKucDj+Gr91sm45AVA7eCeM00S9m5hW044o3b3PgMRG/S/QYCFX7yBL1PyI+FGqDhUTIqxqruJMswzeCm9JGMbnV25PG01Gxoc4Xehd/Qu7XdPuWDGW0nxOnt1lZP34NBslBEZx4LnEva6QpxwQkUUcGtFIOswMZ3lXrlHdaXlW6FGpi0wn+VVnJW0YyDhpafAiLrYRTOLPjyWgNlO+8EDXc1gjGm+M3VvcVB5/F1Yl+eBOTM5B1+8jSp34md8BSNPgupSs694/fAwSAjwXQZojnbZ43Ni8IypK4fxGRnZSY2fb1r8vpBNBOXUzUOKQAh4W5+pDXwk75qhCJfArnnbHdJVfybeMGyVfK/XAVaiFzlJmCsS2n4uCpFRQPD2uVfYalEqcno26J+zmPMba8rdrJySu1hf2oBswaFsSKnwwQYU++pJHC9qoD2RzR/OeRA2HFCi4Eo5ENT4jIU62iVJIC472dVqgXBRoaE6Pp9wGGrwmeK9l0UnyyJuuA6QmIwohj6H3I4DwBF6E7HXhFccaA7O40TJBoBFvaQgbjPs0tlhcl8PiZrShu0wkeXQoojjQPWCGP/GZxJjA3aJQSLLPLCoXPlaT83PbpX81TH90QQhXZUk+wvLPo9VSFZS+1Col/zCoAJsO+O9GmsxY99+TysIQE3d+PgfPV3qSiTfcPX5eA3nAWgY0nTl7suFF/eFsQRzR+PQoSbpEDRuB3kPbnzf0hbUAdFt7Iu1FNjfJin7i3eGLcOjintSwCiUVRDgcO+c1LKJcBiQ2S0y5Rw1FqviP7koHAGEF0ZBthWSAM2rGYx3sgrhVvYoyHbMZk766q0wsufuImUUyVQsrnIexW7BATGLswipdgx+66A3Kk8y5ynHFNhBvRGSdGyO2v7/+Pe8/7roeHSo5756wdJRTnE8CJuyqqhkt3UPZuutHAGgeT5Qokzo16AIZyJ4VWzns03jdCDkRqNdGcTaAxjViUA9cM+Mf9OuqpIhM2cgJ+ox0I5FJOVQy7TkrfAOsYvuSZTk01sALL6skVYWAujrkWpk1wV29G1NdVg6Qpvr4ptDvkNhpCLSghcIO9e0LjK4+tqlG6SZxS4B4ClG8gNmeLJecgQQ","status":0,"msg":""}

            dy_avg = decrypt(datas['data'])
            data.append({'name': name, f'{year}': dy_avg})
            # 将关键词，抖音搜索指数，写入csv中，平台类别抖音为1
            save_list(data, f'{year}.csv', ['name', f'{year}'])
            # browser.close()
        except:
            raise ValueError(i, name)

    # while True:
    #     data = []
    #     for i in range(997, 1000):
    #         name = pf.values[i][2]
    #         data.append(name)
    #         if len(data) == 5:
    #             p = ','.join(data)
    #             url = f'https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword={p}&appName=aweme'
    #             print(url)
    #             data.clear()
    #             aaaa = 'debugger'




        'https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword=%E6%A1%90%E4%B9%A1%E6%A7%9C%E6%9D%8E%2C%E5%A4%A7%E5%AE%81%E7%BA%A2%E7%9A%AE%E5%B0%8F%E7%B1%B3%2C%E6%A2%A7%E6%A1%90%E5%B1%B1%E8%8D%AF%2C%E5%B9%B3%E9%A1%BA%E6%BD%9E%E5%85%9A%E5%8F%82%2C%E6%B0%B8%E5%92%8C%E6%9D%A1%E6%9E%A3&appName=aweme'
        'https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword=大宁红皮小米,梧桐山药,平顺潞党参,永和条枣,莫力达瓦苏子&appName=aweme'