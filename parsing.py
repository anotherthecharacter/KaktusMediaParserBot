import requests
from bs4 import BeautifulSoup as bs


def get_soup(url: str) -> bs:
    """
    Принимает ссылку, отправляет запрос.
    Возвращает объект BeautifulSoup.
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}
    html = requests.get(url, headers=headers)

    return bs(html.text, 'lxml')


def news_collect() -> list:
    from datetime import datetime
    """
    Собирает ежедневно новости, пока их количество не достигнет 20. 
    """
    news = []
    day = datetime.now().strftime('%d')  # сегодняшний день

    while len(news) < 20:
        soup = get_soup('https://kaktus.media/?lable=8&date=2022-10-' + day + '&order=time')
        news.extend(soup.find_all('div', {'class': 'Tag--article'}))
        day = str(int(day) - 1)
    
    return news


def get_description(url: str) -> str:
    """
    Принимает ссылку с новостной статьёй.
    Возвращает её текст.
    """
    soup = get_soup(url)
    description = soup.find('div', {'class': 'BbCode'})

    while description.find('div'):
        description.find('div').replace_with('\n')

    return description.text


def get_data(news: list) -> dict:
    """
    Форматирует данные каждой статьи из списка новостей в словарь.
    """
    data = {}
    id_ = 0

    for single_n in news:
        id_ += 1
        title = single_n.find('a', {'class': 'ArticleItem--name'}).text.strip()
        link_and_photo = single_n.find('a', {'class': 'ArticleItem--image'})
        link = link_and_photo.get('href')
        photo = link_and_photo.find('img').get('src')
        description = get_description(link)

        data.update({str(id_): {'title': title, 'photo': photo, 'description': description}})

        if id_ == 20 :
            break
    
    return data
