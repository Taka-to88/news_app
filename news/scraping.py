import requests
from bs4 import BeautifulSoup
import re
import time
from .models import News

from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler

# 検索ワードのURL特定(本日)


def get_news():
    year = datetime.datetime.today().strftime('%Y')
    month = datetime.datetime.today().strftime('%-m')
    day = datetime.datetime.today().strftime('%-d')
    keyword = "大谷翔平"
    url = 'https://www.yomiuri.co.jp/web-search'
    params = {'st': '1', 'wo': keyword, 'ac': 'srch', 'ar': '1', 'fy': year,
              'fm': month, 'fd': day, 'ty': year, 'tm': month, 'td': day}
    res = requests.get(url, params=params)

    # 検索一覧の読み込み
    soup = BeautifulSoup(res.text, "html.parser")
    elems = soup.select("div.search-article-list > ul")
    elems = elems[0].find_all("h3")

    news_links = [elem.a["href"] for elem in elems]

    for news_link in news_links:
        news_res = requests.get(news_link)
        news_soup = BeautifulSoup(news_res.text, "html.parser")

        # 画像リンクの取得
        img_link = news_soup.find(class_=re.compile(
            "wp-caption none thumbnails-left"))
        img_url = "https://www.yomiuri.co.jp" + \
            img_link.find('img').get("src")
        # print(news_url)
        news_img = requests.get(img_url)

        # print(news_soup.title.text)
        news_title = news_soup.title.text
        # print(news_soup.time.text)
        news_time = news_soup.time.text
        # print(news_link)

        # class属性の値は、サイトを確認して最新の値を設定する必要があります
        detail_text = news_soup.find(class_=re.compile("p-main-contents"))
        news_text = detail_text.text

        # print(detail_text.text if hasattr(
        #     detail_text, "text") else '', end="\n\n\n\n")

        time.sleep(1)

        News.objects.create(title=news_title, link=news_link,
                            published=news_time, body=news_text, image=news_img)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_news, 'cron',
                      hour=23, minute=55)  # 毎日23時55分に実行

    scheduler.start()


print('Update!')
