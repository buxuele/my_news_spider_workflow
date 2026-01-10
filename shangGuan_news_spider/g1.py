import os
import csv
import time
import requests
from datetime import datetime

### 此文件，仅仅是测试看看 api 返回了什么

# 1. 配置请求头 (根据您提供的信息)
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',  # 关键：表单提交格式
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Referer': 'https://www.jfdaily.com/staticsg/home',
    'Origin': 'https://www.jfdaily.com',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
    # Cookie 可以根据需要添加，通常 API 不需要强 Cookie 验证，如果失败请取消下面注释填入
    # 'Cookie': '您的Cookie字符串'
}


def get_jfdaily_data(max_pages=5):
        url = 'https://www.jfdaily.com/news/homeMoreNews'
        current_page = 1

        # 循环爬取
        for page in range(1, max_pages + 1):
            print(f"\n正在爬取第 {page} 页...")

            # 初始化参数
            # 第一次请求使用当前时间戳
            current_last_time = int(time.time() * 1000)

            # 3. 构造 POST 参数
            # 注意：上观新闻 API 的 page 参数似乎用于记录，核心翻页逻辑依赖 lastpublishtime
            payload = {
                'page': page,
                'lastpublishtime': current_last_time
            }

            # 4. 发送 POST 请求 (使用 data= 而不是 json=)
            resp = requests.post(url, headers=headers, data=payload, timeout=10)

            if resp.status_code != 200:
                print(f"请求失败，状态码: {resp.status_code}")
                break

            # 解析 JSON
            res_json = resp.json()
            print(f"响应数据: {res_json}")
            time.sleep(2)



if __name__ == "__main__":

    get_jfdaily_data(max_pages=3)