import time
import requests
from bs4 import BeautifulSoup


def continue_crawl(search_history, target_url, max_urls=25):
    # O último artigo é o mesmo do target_url
    last_item_equals_target = search_history[-1] == target_url

    # O histórico de busca é maior que 25(Limite)
    more_than_25_urls = len(search_history) > max_urls

    # Foi encontrado um loop na busca
    same_article_loop = search_history[-1] in search_history[:-1]

    if last_item_equals_target or more_than_25_urls or same_article_loop:
        return False

    return True


def find_first_link(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    content_div = soup.find(class_='mw-parser-output')
    for element in content_div.find_all('p', recursive=False):
        element_link = element.find('a', recursive=False)

        if element_link:
            return "https://en.wikipedia.org{}".format(element_link.get('href'))


def web_crawler():
    article_chain = ['https://en.wikipedia.org/wiki/Phelps_Farms_Historic_District']
    url_target = 'https://en.wikipedia.org/wiki/Philosophy'

    while continue_crawl(article_chain, url_target):
        first_link = find_first_link(article_chain[-1])
        article_chain.append(first_link)
        time.sleep(2)
        print(article_chain)


if __name__ == '__main__':
    web_crawler()
