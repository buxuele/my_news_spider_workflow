import os
import csv
import time
import requests
from datetime import datetime, timedelta

# 请求头
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',  # 响应头要求 Content-Type
    'Referer': 'https://www.thepaper.cn/',  # 引荐来源，遵循 strict-origin-when-cross-origin
    'Origin': 'https://www.thepaper.cn'  # 跨域请求需要 Origin
}

def get_thepaper_data(file_name='peng_pai_400.csv', max_pages=100, channel_id='-8'):
    """
    爬取澎湃新闻数据，保存到 CSV 文件
    参数：
        file_name: 输出 CSV 文件名
        max_pages: 最大爬取页数
        channel_id: 新闻频道 ID
    """
    # 检查文件是否存在
    has_file = os.path.exists(file_name)

    # 打开 CSV 文件，追加模式
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        columns = ['title', 'url', 'time', 'source']
        writer = csv.DictWriter(file, fieldnames=columns)
        if not has_file:
            writer.writeheader()

        # 计算 startTime（当前时间戳）
        current_time = int(time.time() * 1000)  # 当前毫秒时间戳
        start_time = current_time  # 使用此时此刻的时间

        # 爬取数据
        for page in range(1, max_pages + 1):
            time.sleep(1)  # 请求间隔

            payload = {
                'channelId': channel_id,
                'excludeContIds': [],  # 留空，需根据实际需求调整
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
            # print(f"页面 {page} 响应：{ret}")

            news_list = ret['data']['list']
            for item in news_list:
                # print(item)
                news = {}
                news['title'] = item.get('name', '')
                news['url'] = f"https://www.thepaper.cn/newsDetail_forward_{item.get('originalContId', '')}"
                news['time'] = item.get('pubTimeLong', '')
                news['source'] = item.get('authorInfo', {}).get('sname', '澎湃新闻')

                # 转换时间格式（如果 API 返回时间戳）
                news['time'] = datetime.fromtimestamp(news['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

                # 直接写入，不去重
                writer.writerow(news)
                print(news)

            start_time = ret["data"]['startTime']  # 更新 startTime
            print()


if __name__ == "__main__":
    get_thepaper_data(file_name='peng_pai_news.csv', max_pages=3, channel_id='-8')

