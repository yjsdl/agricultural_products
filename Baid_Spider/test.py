# -*- coding: utf-8 -*-
import pandas as pd
import os

# pf = pd.read_excel('./全国农产品地理标志登记汇总表（截至2022年2月25日）(1).xlsx', dtype=str, header=1)
# print(pf)

# 保存到csv文件
def save_list(data, file, name):
    # desk = os.path.join(os.path.expanduser('~'), 'Desktop')
    # 当前文件夹
    file_path = r'F:\农产品搜索指数\Baid_Spider\地理标识.csv'
    if os.path.isfile(file_path):
        df = pd.DataFrame(data=data)
        df.to_csv(file_path, encoding="utf-8", mode='a', header=False, index=False)
    else:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df = pd.DataFrame(data=data, columns=name)
        df.to_csv(file_path, encoding="utf-8", index=False)


pf = pd.read_csv(r'F:\农产品搜索指数\Baid_Spider\地理标识.csv', dtype=str).fillna('')
pf1 = pd.read_csv(r'F:\农产品搜索指数\Baid_Spider\最终地理大米.csv', dtype=str)
sha = pf.shape[0]
data = []
j = 1
for i in range(0, 135):
    name = pf.values[i][1]
    if not os.path.exists(fr'F:\农产品搜索指数\Baid_Spider\地理产品大米\{name}.csv'):
        print(name)