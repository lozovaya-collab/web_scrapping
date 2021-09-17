from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests as req
from bs4 import BeautifulSoup


options = Options()
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)
driver_article = webdriver.Chrome(options=options)

driver.get('https://cyberleninka.ru/search?q=веб%20скрапинг')

results = driver.find_element_by_class_name('list').find_elements_by_tag_name('li')

linkArray = []
for i in range(len(results)):
    link = results[i].find_element_by_tag_name('h2').find_element_by_tag_name('a').get_attribute("href")
    linkArray.append(link)


h1 = []
key_words_ALL = []
authors_ALL = []
authors = []
key_words = []



ans = req.get(linkArray[0])
print(linkArray[0])
soup = BeautifulSoup(ans.text, 'lxml')
arr = soup.findAll('span', {'class': 'hl to-search'}, title=True)
h1.append(soup.h1.i.get_text())
for i in range(len(arr)):
    key_words.append(arr[i].get_text())
key_words_ALL.append(key_words)
driver_article.get(linkArray[0])

dataAuthors = driver_article.find_element_by_class_name('author-list').find_elements_by_tag_name('li')

for i in range(len(dataAuthors)):
    authors.append(dataAuthors[i].text)
authors_ALL.append(authors)
driver_article.close()




driver.close()
