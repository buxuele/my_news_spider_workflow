import os
import csv
import time
import requests
from datetime import datetime, timedelta

# 请求头
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Referer': 'https://www.thepaper.cn/',
    'Origin': 'https://www.thepaper.cn'
}

def get_thepaper_data(max_pages=100, channel_id='-8'):
    """
    爬取澎湃新闻数据，保存到以日期时间命名的 CSV 文件
    参数：
        max_pages: 最大爬取页数
        channel_id: 新闻频道 ID
    """
    # 创建 csv_data 目录
    os.makedirs('csv_data', exist_ok=True)

    # 生成文件名，格式如 peng_pai_news_20250611_213300.csv
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'csv_data/peng_pai_news_{timestamp}.csv'

    # 打开 CSV 文件，追加模式
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        columns = ['title', 'url', 'time', 'source']
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()  # 每次都写入表头，因为是新文件

        # 计算 startTime（当前时间戳）
        current_time = int(time.time() * 1000)  # 当前毫秒时间戳
        start_time = current_time

        # 爬取数据
        for page in range(1, max_pages + 1):
            time.sleep(1)  # 请求间隔

            payload = {
                'channelId': channel_id,
                'excludeContIds': [],
                'province': '',
                'pageSize': 20,
                'startTime': start_time,
                'pageNum': page
            }

            url = 'https://api.thepaper.cn/contentapi/nodeCont/getByChannelId'
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            if resp.status_code != 200:
                print(f"请求失败：{url}, 状态码: {resp.status_code}, 页码: {page}")
                break

            ret = resp.json()
            news_list = ret['data']['list']
            for item in news_list:
                news = {}
                news['title'] = item.get('name', '')
                news['url'] = f"https://www.thepaper.cn/newsDetail_forward_{item.get('originalContId', '')}"
                news['time'] = item.get('pubTimeLong', '')
                news['source'] = item.get('authorInfo', {}).get('sname', '澎湃新闻')

                # 转换时间格式
                news['time'] = datetime.fromtimestamp(news['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

                # 写入 CSV
                writer.writerow(news)
                print(news)

            start_time = ret["data"]['startTime']
            print()

if __name__ == "__main__":
    get_thepaper_data(max_pages=3, channel_id='-8')