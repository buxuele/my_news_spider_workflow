import os
import csv
import time
import requests
from datetime import datetime

# url = 'https://www.jfdaily.com/news/homeMoreNews'

# 1. 配置请求头
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Referer': 'https://www.jfdaily.com/staticsg/home',
    'Origin': 'https://www.jfdaily.com',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def get_jfdaily_data(max_pages=5):
    # 2. 创建文件夹和文件
    base_dir = 'shangguan_news'
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'{base_dir}/shangguan_news_{timestamp}.csv'

    print(f"开始爬取，数据将保存至: {file_name}")

    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        columns = ['title', 'url', 'time', 'source']
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        url = 'https://www.jfdaily.com/news/homeMoreNews'

        # --- 关键修正：初始化时间必须在循环外 ---
        # 第一次请求使用当前系统时间
        current_last_time = int(time.time() * 1000)

        # 循环爬取
        for page in range(1, max_pages + 1):
            print(f"\n正在爬取第 {page} 页 (lastpublishtime: {current_last_time})...")

            # 3. 构造 POST 参数
            payload = {
                'page': page,
                'lastpublishtime': current_last_time
            }

            try:
                # 4. 发送 POST 请求
                resp = requests.post(url, headers=headers, data=payload, timeout=10)

                if resp.status_code != 200:
                    print(f"请求失败，状态码: {resp.status_code}")
                    break

                # 解析 JSON
                res_json = resp.json()

                # --- 关键修正：根据你的返回结果，数据在 'object' 字段中 ---
                news_list = res_json.get('object', [])

                if not news_list:
                    print("本页无数据或已到达底部，停止爬取。")
                    break

                # 5. 遍历并写入 CSV
                for item in news_list:
                    news = {}
                    news['title'] = item.get('title', '').strip()

                    # 拼接 URL
                    if 'id' in item:
                        news['url'] = f"https://www.jfdaily.com/news/detail?id={item['id']}"
                    else:
                        news['url'] = ''

                    # 处理时间 (毫秒时间戳转字符串)
                    pub_time_raw = item.get('publishtime', 0)
                    if pub_time_raw:
                        news['time'] = datetime.fromtimestamp(pub_time_raw / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        news['time'] = ''

                    # 获取来源 (优先用 source，没有则用 author)
                    news['source'] = item.get('source') or item.get('author', '上观新闻')

                    # 写入一行
                    writer.writerow(news)
                    print(f"已抓取: {news['title']}")

                # 6. 更新下一页的时间游标
                # 取出列表中最后一条新闻的时间，赋给 current_last_time
                if news_list:
                    last_item = news_list[-1]
                    last_time = last_item.get('publishtime')
                    if last_time:
                        current_last_time = last_time
                    else:
                        # 如果没有时间戳，防止死循环，稍微减去一点时间或保持不变(视API特性而定)
                        print("警告：无法获取最后一条数据的时间戳")

                # 礼貌延时
                time.sleep(2)

            except Exception as e:
                print(f"发生异常: {e}")
                break


if __name__ == "__main__":
    get_jfdaily_data(max_pages=5)

