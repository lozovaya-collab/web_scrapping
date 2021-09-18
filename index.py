# подключаем необходимые библиотеки
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests as req
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException   
import json, io

# проверка на наличие элемента на странице
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# настрокйка веб-драйвера
def create_driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver

# ищем все статьи на Киберленике
def find_all_articles(req):
    driver_request = create_driver()
    driver_request.get('https://cyberleninka.ru/search?q=' + req)

    results = driver_request.find_element_by_class_name('list').find_elements_by_tag_name('li')

    urlArray = [] # ссылки на статьи
    for i in range(len(results)):
        url = results[i].find_element_by_tag_name('h2').find_element_by_tag_name('a').get_attribute("href")
        urlArray.append(url)

    print('Статей найдено: ', len(urlArray))

    return urlArray

# чекаем статью и вытаскиваем всю необходимую информацию
def check_article(url):
    authors = [] 
    
    ### парсим с помощью BeautifulSoup ####
    ans = req.get(url)
    soup = BeautifulSoup(ans.text, 'lxml')

    # название статьи 
    title = soup.h1.i.get_text()

    # ключевые слова
    key_words = []
    keys_span = soup.findAll('span', {'class': 'hl to-search'}, title=True)
    for i in range(len(keys_span)):
        key_words.append(keys_span[i].get_text())

    # источник
    source = soup.select('div[class="half"] > span > a')[0].get_text()

    # аннотация
    for span in soup.find_all("span", {'class':'hl to-search'}):
        span.decompose()
    description = soup.select('p[itemprop="description"]')[0].get_text()

    ### парсим с помощью webDriver ###
    driver_article = create_driver()
    driver_article.get(url)

    # авторы
    authors = [] 
    dataAuthors = driver_article.find_element_by_class_name('author-list').find_elements_by_tag_name('li')

    for i in range(len(dataAuthors)):
        authors.append(dataAuthors[i].text)
        
    # проверка на возможность скачать
    path = "//a[@id='btn-download']"
    isDownload = check_exists_by_xpath(driver_article, path)

    info_about_article = {
        "article": url,
        "title": title,
        "authors": authors,
        "key words": key_words,
        "publication": source,
        "summary": description,
        "available to download": isDownload
    }
    return info_about_article

# информация по всем найденным статьям
def get_articles(urls):

    all_information = []
    for index in range(len(urls)):
        number_of_article = index + 1
        status = f"Парсинг {number_of_article} статьи"
        print(status)

        info_article = check_article(articles_for_user[index])
        all_information.append(info_article)

    return all_information

# делаем запрос на Киберленике
user_request = input("Какие статьи вас интересуют: ")
print('Запрос обработан')

articles_for_user = find_all_articles(user_request)
info = get_articles(articles_for_user)

# результаты парсинга записать в json
with io.open('articles.json','w',encoding='utf-8') as f: 
    json.dump(info, f, indent=4, ensure_ascii=False)
