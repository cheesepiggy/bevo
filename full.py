import requests
from bs4 import BeautifulSoup


url = "https://www.bevo.com/"
r = requests.get(url, timeout=(0.95, None))
soup = BeautifulSoup(r.text, "lxml")
souppage = soup.find("ul", {'class': 'navigation--list container'})
souppage2 = souppage.findAll("li", {'class': 'navigation--entry'})[2:]

url_list = []
for tags in souppage2:
    url = [tags.findNext('a').get('href')]
    url_list.append(url)

url_list2 = []
for url in url_list:
    r = requests.get(url[0], timeout=(0.95, None))
    soup = BeautifulSoup(r.text, "lxml")
    souppage = soup.find("div", {'class': 'listing--categories'})
    categories = souppage.findAll("div", {'class': 'category--box'})
    for url in categories:
        url = url.findNext('a').get('href')
        url_list2.append(url)

url_list_for_parsing = []
for url in url_list2:
    r = requests.get(url, timeout=(0.95, None))
    soup = BeautifulSoup(r.text, "lxml")
    pages_count = soup.find("a", {'title': 'Letzte Seite'})
    if pages_count is not None:
        # pages_count = soup.find("a", {'title': 'Letzte Seite'})
        pages_count = int(pages_count.text)
        for page_index in range(1, pages_count + 1):
            url_list_for_parsing.append(url + '?p=' + str(page_index)) #да, я помню про f строки
    else:
        url_list_for_parsing.append(url)
direct_links = []

for url in url_list_for_parsing:
    r = requests.get(url, timeout=(0.95, None))
    soup = BeautifulSoup(r.text, "lxml")
    products_list = soup.find("div", {'class': 'listing'})
    products_list = products_list .findAll("div", {'class': 'product--box'})
    for url in products_list:
        url = url.findNext('a').get('href')
        direct_links.append(url)

item_list = [['Code', "Name", "Price"]]
for link in direct_links:
    r = requests.get(link, timeout=(0.95, None))
    soup = BeautifulSoup(r.text, "lxml")
    products = soup.findAll("div", {'class': 'product-variants-accordion--item'})
    name = soup.find('h1', {"class": 'product--title'}).text
    for tag in products:
        item = [tag.find('div', {"class": 'accordion--toggler'}).text,
                str(name + ' (' + tag.find('div', {"class": 'product-variant--group'}).text + ')'),
                tag.find('div', {"class": 'product-variant--price'}).text]
        item_list.append(item)


final_list = [[i.strip("\n\r\n €") for i in item] for item in item_list]


with open('bevo_items.csv', 'w', encoding='utf8') as file:
    for row in final_list:
        for string in row:
            if string != row[-1]:
                file.write(str(string) + ",")
            else:
                file.write(str(string))
        file.write("\n")


