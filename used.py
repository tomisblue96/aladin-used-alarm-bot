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
SEND_ERROR_TO_TELEGRAM = 1


def number_filter(text):
    found_nums = filter(str.isdigit, text)
    return int(''.join(found_nums))


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

        # 중고도서 페이지 수집
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.select("td[width='25%']")

        for index, item in enumerate(items):
            # 중고도서 정보 파싱
            book_name = item.select_one("a.bo").previous_sibling + item.select_one("a.bo").text
            book_writer = item.select_one("span.gw").text
            book_price = number_filter(item.select_one("span.gw").next_sibling.text)
            book_sale = item.select_one("span.gw").next_sibling.text \
                         + item.select_one("span.p1_n").previous_sibling \
                         + item.select_one("span.p1_n").text
            book_link = item.select_one("td a")['href']
            book_code = book_link.replace('https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=', '')
            presents.add(book_code)

            # 새로 업데이트된 중고도서일 경우 텔레그렘 메세지 전송
            if not (n == 3 and index > 40):
                if previous and book_code not in previous and book_price >= MAX_PRICE:
                    info = '\n'.join([book_name, book_writer, book_sale, book_link])
                    print(info)
                    bot.sendMessage(chat_id=chat_id, text=info)


def main():
    bot.sendMessage(chat_id=chat_id, text="Hello!")
    while True:
        if SEND_ERROR_TO_TELEGRAM:
            try:
                notice_used()
            except:
                error = '[비싼 알라딘 중고]' + traceback.format_exc().splitlines()[-1]
                print(error)
                error_bot.sendMessage(chat_id=error_chat_id, text=error)
        else:
            notice_used()
        time.sleep(30)


if __name__ == "__main__":
    main()
