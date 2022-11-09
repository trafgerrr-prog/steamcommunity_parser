import requests
import json
import time
import datetime

headers = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.1.985 Yowser/2.5 Safari/537.36"
}
price_buy_order = []
price_sell_order = []
last_price_buy_order = []
last_price_sell_order = []


# 1. !!!!!!!!!!!!!!!!!!!!Переписать методы для того, чтобы можно было парсить разные предметы
#    получить список url на предметы
# 2. попробовать асинхронный парсинг
# 3. написать бота в телегу
# 4. мб что еще


def get_page(url):
  s = requests.Session()
  response = s.get(url=url, headers=headers)

  with open("index.html", "w", encoding="utf-8") as file:
    file.write(response.text)





def get_json(url):
  s = requests.Session()
  response = s.get(url=url, headers=headers)

  with open("result.json", "w", encoding="utf-8") as file:
    json.dump(response.json(), file, indent=4, ensure_ascii=False)


def collect_buy_order(url):
  s = requests.Session()
  response = s.get(url=url, headers=headers)
  data = response.json()

  for i in range(5):
    data_prices = data.get("buy_order_graph")
    data_prices = data_prices[i]
    price_buy_order.append(data_prices[0])


def collect_sell_order(url):
  s = requests.Session()
  response = s.get(url=url, headers=headers)
  data = response.json()

  for i in range(5):
    data_prices = data.get("sell_order_graph")
    data_prices = data_prices[i]
    price_sell_order.append(data_prices[0])


def check_prices(url):
  print("----start----")
  collect_buy_order(url=url)
  collect_sell_order(url=url)

  last_price_buy_order.clear()
  for i in range(5):
    last_price_buy_order.append(price_buy_order[i])
  print(f'Last price_buy_order = {last_price_buy_order}')
  price_buy_order.clear()

  last_price_sell_order.clear()
  for i in range(5):
    last_price_sell_order.append(price_sell_order[i])
  print(f'Last price_sell_order = {last_price_sell_order}')

  # today = datetime.datetime.today()
  # print("----time----")
  # print(today.strftime("%Y-%m-%d-%H.%M.%S"))
  # print("---/time----")

  price_sell_order.clear()

  print("------------------")
  time.sleep(60)

  collect_buy_order(url=url)
  collect_sell_order(url=url)

  # today = datetime.datetime.today()
  # print("----time----")
  # print(today.strftime("%Y-%m-%d-%H.%M.%S"))
  # print("---/time----")

  print(f'Price_buy_order now = {price_buy_order}')
  print(f'Price_sell_order now = {price_sell_order}')
  print("----stop?----")


def send_price(url):
  check_prices(url)

  if price_buy_order[0] >= (last_price_buy_order[1] * 1.5):
    print("!!!------------------!!!")
    today = datetime.datetime.today()
    print("----time----")
    print(today.strftime("%Y-%m-%d-%H.%M.%S"))
    print("---/time----")

    print(f'Резкий буст цен {price_buy_order[0]} --- {last_price_buy_order[1]}')
    print("!!!------------------!!!")
  if (price_buy_order[0] * 1.13) < price_sell_order[0]:
    print("!!!------------------!!!")
    today = datetime.datetime.today()
    print("----time----")
    print(today.strftime("%Y-%m-%d-%H.%M.%S"))
    print("---/time----")

    print(f'Выгодная перепродажа {price_buy_order[0]} --- {price_sell_order[0]}')
    print("!!!------------------!!!")



  # for i in range(len(list)):
  #   collect_buy_order(list[i])
  #   print(f'{i} предмет из {len(list)} Цены: {price_buy_order}')


def main():
  pass
  # test()

  # get_item_nameid("https://steamcommunity.com/market/listings/730/Sticker%20%7C%20broky%20%28Champion%29%20%7C%20Antwerp%202022")


  # get_page(
  #   url="https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=176312142&two_factor=0")
  # get_json(
  #   url="https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=176312142&two_factor=0")
  # get_json(
  #   url="https://steamcommunity.com/market/search/render/?query=&start=0&count=10&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_ItemSet[]=any&category_730_ProPlayer[]=any&category_730_StickerCapsule[]=any&category_730_TournamentTeam[]=any&category_730_Weapon[]=any&category_730_StickerCategory[]=tag_PlayerSignature&category_730_StickerCategory[]=tag_TeamLogo&category_730_Tournament[]=tag_Tournament19")
  # collect_buy_order(
  #   url="https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=176312142&two_factor=0")

  # while True:
  #   send_price(
  #     "https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=176312142&two_factor=0")


if __name__ == "__main__":
  main()
