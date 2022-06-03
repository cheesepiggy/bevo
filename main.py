import requests
from bs4 import BeautifulSoup
import lxml


url = "https://www.bevo.com/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
souppage = soup.find("ul", {'class': 'navigation--list container'})
souppage2 = souppage.findAll("li", {'class': 'navigation--entry'})[2:]

url_list = []
for tags in souppage2:
    url = [tags.findNext('a').get('href')]
    url_list.append(url)

url_list2 = []
for url in url_list:
    r = requests.get(url[0])
    soup = BeautifulSoup(r.text, "lxml")
    souppage = soup.find("div", {'class': 'listing--categories'})
    categories = souppage.findAll("div", {'class': 'category--box'})
    for url in categories:
        url = url.findNext('a').get('href')
        url_list2.append(url)

url_list_for_parsing = []
for url in url_list2:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    pages_count = soup.find("a", {'title': 'Letzte Seite'})
    if pages_count is not None:
        # pages_count = soup.find("a", {'title': 'Letzte Seite'})
        pages_count = int(pages_count.text)
        for page_index in range(1, pages_count + 1):
            url_list_for_parsing.append(url + '?p=' + str(page_index)) #да, я помню про f строки
    else:
        url_list_for_parsing.append(url)

# url_list_for_parsing = ['https://www.bevo.com/beregnung/tropfberegnung?p=1', 'https://www.bevo.com/beregnung/tropfberegnung?p=2']


