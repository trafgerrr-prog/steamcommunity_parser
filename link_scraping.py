import requests
import json
import mysql.connector
import random
from bs4 import BeautifulSoup
from prices_scraping import *

headers = {
  "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.1.985 Yowser/2.5 Safari/537.36"
}


def get_jsons():
  for i in range(60):
    response = requests.Session().get(
      url=f'https://steamcommunity.com/market/search/render/?query=&start={i * 10}&count=10&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_ItemSet[]=any&category_730_ProPlayer[]=any&category_730_StickerCapsule[]=any&category_730_TournamentTeam[]=any&category_730_Weapon[]=any&category_730_StickerCategory[]=tag_PlayerSignature&category_730_StickerCategory[]=tag_TeamLogo&category_730_Tournament[]=tag_Tournament19',
      headers=headers)

    with open(f'result_{i}.json', "w", encoding="utf-8") as file:
      json.dump(response.json(), file, indent=4, ensure_ascii=False)

    print(f'Полученно {i + 1} json страниц из 60')
    s = random.randint(10, 60)
    print(f'Время ожидания: {s}\n')
    time.sleep(s)


def get_item_nameid(url):
  s = random.randint(20, 30)
  print(f'Время ожидания: {s}\n')
  time.sleep(s)
  site_txt = requests.get(url).text
  index = site_txt.split(" ").index("initial")
  print(f'nameid: {site_txt.split(" ")[index - 2]}')

  s = random.randint(0, 1)
  if s == 1:
    s = random.randint(20, 60)
    print(f'Время ожидания: {s}\n')
    time.sleep(s)
  else:
    s = random.randint(30, 45)
    print(f'Время ожидания: {s}\n')
    time.sleep(s)

  return site_txt.split(" ")[index - 2]


def list_url():
  with open("items.json") as read_file:
    data = json.load(read_file)
  list = data.values()
  list = ("\n".join(list)).split()
  return list


def full_db():
  list = list_url()
  myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="steam_items")
  cur = myconn.cursor()

  for j in range(len(list)):
    sql = "insert into id_name_url_nameid(url, nameid) values(%s, %s)"
    val = (list[j], get_item_nameid(list[j]))

    try:
      # inserting the values into the table
      cur.execute(sql, val)

      # commit the transaction
      myconn.commit()

    except:
      myconn.rollback()



def get_names_links():
  link_items = []
  name_items = []
  for i in range(60):
    with open(f'result_{i}.json') as file:
      data = json.load(file)
    print(f'\n{i + 1} круг из 60 кругов\n{data}')

    soup = BeautifulSoup(data.get("results_html"), "lxml")
    links = soup.findAll("a", class_="market_listing_row_link")
    names = soup.findAll("div", class_="market_listing_row market_recent_listing_row market_listing_searchresult")
    for link in links:
      link_items.append(link.get("href"))
    for name in names:
      name_items.append(name.get("data-hash-name"))

    for j in range(len(link_items)):
      print(f'Предмет: {name_items[j]}  Линка: {link_items[j]}')

  dictionary_items = dict(zip(name_items, link_items))
  with open('items.json', 'w', encoding="utf-8") as file:
    json.dump(dictionary_items, file, indent=4, ensure_ascii=False)




def main():
  pass
  # get_jsons()
  # get_names_links()
  # full_db()

if __name__ == "__main__":
  main()
