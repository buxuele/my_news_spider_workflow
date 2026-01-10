

### 新增一个爬虫， 上观新闻 
2026年1月10日19:54:12


### git 操作重点的地方

git pull --rebase  # 获取远程更新并保持线性历史
git push           # 推送你的修改


### workflow 几种时间
- cron: '0 */5 * * *'  #  每5个小时触发一次
- cron: '0 4 * * *'    #  每天中午12点触发一次


### 此项目的远程地址是：
https://github.com/buxuele/my_news_spider_workflow


### 目的
GitHub Actions  +  爬虫自动化, 爬取 澎湃新闻， 保存为 csv


#### 我的要求：

帮我写一个完整的 GitHub Actions 工作流，即， yml 文件， 
而且写上注释，让别人看懂。

包含：
- 表示每2分钟触发，，每2分钟运行一次， 而且打印出运行时间。当前调试阶段先这样，后面我再改！
- 先安装依赖： pip install -r requirements.txt, 第一次运行时，安装依赖。其他时候，直接运行。
- Workflow 中运行 Python 爬虫脚本， 代码文件名字是： 项目根目录/news_spider/peng_pai_02.py
  即 python  项目根目录/news_spider/peng_pai_02.py


