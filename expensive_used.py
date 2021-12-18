import requests
import traceback
import time

import telegram
from bs4 import BeautifulSoup


# 텔레그램 토큰값
bot = telegram.Bot(token='1809686931:AAHj4R107m6NKYw-Sd0Ein50RVlblNZyvoQ')
my_something_bot = telegram.Bot(token='1912641898:AAFAJWwPQ7jr5QHWl2I3Iwmj4Sad7UbokgQ')
chat_id = 1033055927

# 세션 만들기
session = requests.session()
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',}

presents = set()
previous = set()

MAX_PRICE = 22000


while True:
    try:
        # 딕셔너리 업데이트
        previous = set(presents)
        presents = set()

        # 마이페이지 접근
        items = []
        for n in range(1, 4):
            url = f"https://www.aladin.co.kr/shop/common/wnew.aspx?ItemType=100&BranchType=6&ViewRowsCount=48&ViewType=Simple&PublishMonth=0&SortOrder=6&page={n}&UsedShop=0&PublishDay=84&NewType=new&SearchOption=&IsDirectDelivery=0&QualityType=&OrgStockStatus="
            response = session.get(url, headers=header)
            response.raise_for_status()

            # HTML분석
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.select("td[width='25%']")
            for index, item in enumerate(items):
                name = ' '.join([item.find("td", valign="top").text.split(" ")[0], item.find("a", "bo").text.strip()])
                span = [n.text.strip() for n in item.select("span")][:-1]
                price = int(span[-2].replace(",", ""))
                info = '\n'.join([name, span[-3].replace(" | ", "\n"), '→'.join(span[1:]), item.find('a')['href']])
                # print(info, price)
                if not (n == 3 and index > 40):
                    if previous and name not in previous and price >= MAX_PRICE:
                        print(info)
                        bot.sendMessage(chat_id=chat_id, text=info)
                presents.add(name)

        print(presents)
        print(previous)
        print(len(presents), len(previous))

        time.sleep(30)
    except:
        error = '[비싼 알라딘 중고]' + traceback.format_exc().splitlines()[-1]
        print(error)
        my_something_bot.sendMessage(chat_id=chat_id, text=error)


