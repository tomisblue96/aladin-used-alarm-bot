import requests
import traceback
import time

import telegram
from bs4 import BeautifulSoup

from config import Config

# 텔레그램 토큰값
bot = telegram.Bot(token=Config.telegram_tokens['bot_token'])
error_bot = telegram.Bot(token=Config.telegram_tokens['error_bot_token'])
chat_id = Config.telegram_tokens['chat_id']

# 세션, 헤더 초기화
session = requests.session()
header = {
        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36', }

presents = set()
previous = set()


def login():
    url = "https://www.aladin.co.kr/m/mlogin.aspx"

    data = {
        "Email": Config.aladin_account['id'],
        "Password": Config.aladin_account['password'],
        "Action": 1,
        "snsUserId": 0,
        "snsType": 0,
        "snsAppId": 1
    }
    res = session.post(url, data=data, headers=header)

    # 로그인 실행
    res.raise_for_status()


def update_catalog():
    global previous, presents
    # 딕셔너리 업데이트
    previous, presents = presents, set()

    # 마이페이지 접근
    for n in range(1, 1000):
        url = f"https://www.aladin.co.kr/m/mbest.aspx?isOpen=0&isAutoRemove=1&IsBuyGoods=2&HasUsedType=2&HasStock=2&isSaveBasketSet=1&SortOrderSet=1&OffCode=&OnlineOffCode=&SearchSubBarcode=&IsLibrarian=0&SortOrder=1&BranchType=0&CID=0&page={n}&SearchWord=&BestType=savebasket"
        response = session.get(url, headers=header)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        if soup.find("div", "keep_box"):
            break

        # 책 정보를 추출하여 이전에 없었을 경우 텔레그렘 봇에게 전달
        items = soup.select("ul.b_list2")
        for index, item in enumerate(items):
            book_name = item.select_one("li:nth-of-type(1)").text
            book_writer = item.select_one("li:nth-of-type(2)").text
            publisher, book_date, _ = item.select_one("li:nth-of-type(3)").text.split(' | ')
            book_prices = item.select_one("li:nth-of-type(4)").text
            book_link = 'https://www.aladin.co.kr/shop/UsedShop/w' + item['onclick'][43:-2]
            if previous and book_name not in previous:
                book_info = [book_name, book_writer, publisher, book_date, book_prices, book_link]
                bot.sendMessage(chat_id=chat_id, text='\n'.join(book_info))
            presents.add(book_name)

    print(presents)
    print(previous)


def main():
    login()
    while True:
        try:
            update_catalog()
        except:
            error = '[나의 알라딘 직배송]' + traceback.format_exc().splitlines()[-1]
            error_bot.sendMessage(chat_id=chat_id, text=error)
        time.sleep(10)


if __name__ == "__main__":
    main()
