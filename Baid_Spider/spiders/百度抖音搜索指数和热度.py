import json
import base64
import random
import re
import os
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from Crypto.Cipher import AES
from selenium import webdriver
import csv
import time


# chrome_options = Options()
# chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
# browser = webdriver.Chrome(executable_path=r'E:\Google\Chrome\Application\chromedriver.exe',
#                            options=chrome_options)  # executable执行webdriver驱动的文件

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
class Browser():
    def __init__(self):
        chrome_options = Options()      # 创建options对象
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
        chrome_options.add_argument('log-level=2')  # 日志级别

        self.browser = webdriver.Chrome(r'D:\python38\chromedriver.exe', options=chrome_options)     # 打开chromedriver
        self.browser.get('https://trendinsight.oceanengine.com/arithmetic-index')       # 打开巨量抖音算数指数网址

    """
    获取接口签名的方法
    """

    def signature(self, keyword, start_date, end_date):
        # 运行script
        sign_url = self.browser.execute_script('''
                    function queryData(url) {
                       var p = new Promise(function(resolve,reject) {
                           var e={"url":"https://trendinsight.oceanengine.com/api/open/index/get_multi_keyword_hot_trend",
                                    "method":"POST",
                                    "data" : '{"keyword_list": ["%s"],"start_date": "%s","end_date": "%s","app_name": "aweme"}'};
                            var h = new XMLHttpRequest;h.open(e.method, e.url, true);
                            h.setRequestHeader("accept","application/json, text/plain, */*");  
                            h.setRequestHeader("content-type","application/json;charset=UTF-8");
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

    def close(self):
        self.browser.close()
        self.browser.quit()

# 获得指定时间段内抖音搜索指数相关数据（2021-01-01：2021-12-31）
def get_data(keyword, start_date, end_date):
    # 请求头文件
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-length": "101",
        "content-type": "application/json",
        "cookie": "MONITOR_WEB_ID=49275518-9c3e-48ba-9230-73137936ebee; passport_csrf_token=920efda20659e00e48b71fda82c30e11; passport_csrf_token_default=920efda20659e00e48b71fda82c30e11; s_v_web_id=verify_l6vy1vn3_L7ExbVS2_9t6K_4l8B_A9TA_NZEQ32HlJAXU; odin_tt=905cc6c114fdcdee72c6601c98a3ecb303843c0d35966e8cd28cc10520667d55fec6e5772258c621deb1b79c35cfe72eb18408fce3878dda4c2e334e2c15b16b; n_mh=qtVwkZBwdVnXf5NwDs_0LrHTCgRS2GJawV5OKWYHLdI; passport_auth_status=117f140c0c960fa8efe1146e00a0af9a%2C; passport_auth_status_ss=117f140c0c960fa8efe1146e00a0af9a%2C; sso_auth_status=4b315ce5b9aeba8ff3e554b98c0024bc; sso_auth_status_ss=4b315ce5b9aeba8ff3e554b98c0024bc; passport_auth_status_count=e5d3c2e9a754746d0a710270441c13a2%2C; passport_auth_status_ss_count=e5d3c2e9a754746d0a710270441c13a2%2C; sid_guard_count=749f54e17da25e827ec6e01973cd4a09%7C1660639802%7C5184000%7CSat%2C+15-Oct-2022+08%3A50%3A02+GMT; uid_tt_count=5f4ca59a03b5d9419637fe4b5e3e73fa; uid_tt_ss_count=5f4ca59a03b5d9419637fe4b5e3e73fa; sid_tt_count=749f54e17da25e827ec6e01973cd4a09; sessionid_count=749f54e17da25e827ec6e01973cd4a09; sessionid_ss_count=749f54e17da25e827ec6e01973cd4a09; sid_ucp_v1_count=1.0.0-KGJmOWFiNTBmY2YyMzBiNjBmZWJhZmE1NmFiZWM5ZjI1NTBlZTAxMmQKGAjtuLCt-43hBxC6tO2XBhjS3BU4AkDsBxoCbGYiIDc0OWY1NGUxN2RhMjVlODI3ZWM2ZTAxOTczY2Q0YTA5; ssid_ucp_v1_count=1.0.0-KGJmOWFiNTBmY2YyMzBiNjBmZWJhZmE1NmFiZWM5ZjI1NTBlZTAxMmQKGAjtuLCt-43hBxC6tO2XBhjS3BU4AkDsBxoCbGYiIDc0OWY1NGUxN2RhMjVlODI3ZWM2ZTAxOTczY2Q0YTA5; sid_guard=bab86f2612d1ef402c8353c1a3b9e26b%7C1660639809%7C5183993%7CSat%2C+15-Oct-2022+08%3A50%3A02+GMT; uid_tt=f0406bcecfa4634d2b142d646c5c2e67; uid_tt_ss=f0406bcecfa4634d2b142d646c5c2e67; sid_tt=bab86f2612d1ef402c8353c1a3b9e26b; sessionid=bab86f2612d1ef402c8353c1a3b9e26b; sessionid_ss=bab86f2612d1ef402c8353c1a3b9e26b; Hm_lvt_df640d0b13edcfb2bad5f8d5e951c90e=1660639920; _ga_313DD262YW=GS1.1.1660642307.2.0.1660642307.0; gr_user_id=1619545e-b7a1-4232-bf52-c94ce6a03e0f; grwng_uid=fd8ee66f-d9d1-4939-b2e7-0ce4ff08ea86; _ga=GA1.1.1506402603.1660639921; _ga_2M3R5Z77SJ=GS1.1.1660644344.1.0.1660644347.0; ttwid=1%7CC1oBTRnLTyUKnUXg21bj9cJFOMuHkWsnd5TdQFroTes%7C1660696216%7C508f5782ef0bf2e168aeb32e4b3267a8eb00cfe0b8bca1732b0e7e49f80eef4e; Hm_lvt_c36ebf0e0753eda09586ef4fb80ea125=1660527648,1661246228; x-jupiter-uuid=16612462356919600; tt_scid=NVruG99JsiMGb02OH-sL9RmUKVbxJpmOaBXtWnub5i930Covk67WJJ5dViIUj.CFdc65; Hm_lpvt_c36ebf0e0753eda09586ef4fb80ea125=1661309180; _csrf_token=KqZ0l2B02zqccuMscRSsCg00; msToken=g2Mcd9JZdnRa-DSwzKFDoEJKZe5-ygTvPv-KlSvrfcRS_WV1RMqNkgGxAhF4amraJCj7Ac7DzHP7fbu3A-rz_CFjkyGMNGfih1ahxREyLS644oBe8QbHrijBr-irBzc=",
        "origin": "https://trendinsight.oceanengine.com",
        "pragma": "no-cache",
        "referer": "https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword=lx",
        "sec-ch-ua": "\"Google Chrome\";v=\"99\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    # 请求data数据
    data = '{"keyword_list": ["%s"],"start_date": "%s","end_date": "%s","app_name": "aweme"}' % (
        keyword, start_date, end_date)
    # 获取数据所在网址链接
    sign_url = browser.signature(keyword=keyword, start_date=start_date, end_date=end_date)
    # 请求页面响应
    try:
        resp = requests.post(sign_url, headers=headers, data=data.encode(), proxies={})
        doc = resp.json()['data']       # 获取json中data字段
        return doc      # 返回加密数据
    except:
        return ''


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

    # print(keyword, aver_data)
    return aver_data        # 返回抖音日搜索平均值



if __name__ == '__main__':
    # 获取需要查询的关键词
    pf = pd.read_csv(r'F:\农产品搜索指数\Baid_Spider\抖音指数\2019.csv', dtype=str)
    sha = pf.shape[0]
    year = '2018'
    start_date = f'{year}-01-01'   # 起始时间
    end_date = f'{year}-12-31'     # 结束时间

    for i in range(0, sha):
        data = []
        # time.sleep(random.randint(5, 7))
        num = pf.values[i][1]
        # if len(data) == 5:
        #     p = ','.join(data)
        # url = f'https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword={p}&appName=aweme'
        # print(url)
        name = pf.values[i][0]

        # if num != '0':
        #     print(name)

        if num == '0':
            data.append({'name': name, f'{year}': num})
            save_list(data, f'{year}.csv', ['name', f'{year}'])

        elif num != '0':
            browser = Browser()     # 创建Browser对象
            # 获取2021-01-01至2021-12-31时间段内抖音搜索指数日均值
            datas = get_data(name, start_date.replace('-', ''), end_date.replace('-', ''))
            if datas == '':
                dy_avg = 0
            else:
                dy_avg = decrypt(datas)
            print(name, dy_avg)
            data.append({'name': name, f'{year}': dy_avg})
            # 将关键词，抖音搜索指数，写入csv中，平台类别抖音为1
            save_list(data, f'{year}.csv', ['name', f'{year}'])
            browser.close()     # 关闭browse