import requests
import traceback
import time

import telegram
from bs4 import BeautifulSoup

from config import Config

# 텔레그램 토큰값
bot = telegram.Bot(token=Config.telegram_tokens['used_bot_token'])
error_bot = telegram.Bot(token=Config.telegram_tokens['error_bot_token'])
chat_id = Config.telegram_tokens['used_chat_id']
error_chat_id = Config.telegram_tokens['my_chat_id']

# 세션 만들기
session = requests.session()
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', }

presents = set()
previous = set()

MAX_PRICE = 24900


def notice_used():
    global previous, presents
    # 리스트 업데이트
    previous = set(presents)
    presents = set()

    # 마이페이지 접근
    for n in range(1, 4):
        url = f"https://www.aladin.co.kr/shop/common/wnew.aspx?ItemType=100&BranchType=6&ViewRowsCount=48&ViewType=Simple&PublishMonth=0&SortOrder=6&page={n}&UsedShop=0&PublishDay=84&NewType=new&SearchOption=&IsDirectDelivery=0&QualityType=&OrgStockStatus="
        response = session.get(url, headers=header)
        response.raise_for_status()

        # 중고도서 목록 수집
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.select("td[width='25%']")

        for index, item in enumerate(items):
            # print(item.select_one("td a")['href'])
            book_name = item.select_one("a.bo").previous_sibling + item.select_one("a.bo").text
            book_writer = item.select_one("span.gw").text
            book_price = item.select_one("td span.").text \
                         + item.select_one("td span.").next_sibling \
                         + item.select_one("span.p1_n").text
            book_link = item.select_one("td a")['href']
            book_link_code = book_link.replace('https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=', '')

            if not (n == 3 and index > 40):
                if previous and book_link_code not in previous and book_price >= MAX_PRICE:
                    info = '\n'.join([book_name, book_writer, book_price, book_link])
                    print(info)
                    bot.sendMessage(chat_id=chat_id, text=info)

            presents.add(book_link_code)

    print(presents)
    print(previous)


def main():
    while True:
        try:
            notice_used()
        except:
            error = '[비싼 알라딘 중고]' + traceback.format_exc().splitlines()[-1]
            print(error)
            error_bot.sendMessage(chat_id=chat_id, text=error)
        time.sleep(30)


if __name__ == "__main__":
    main()
