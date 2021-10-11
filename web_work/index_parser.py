# подключаем необходимые библиотеки
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json, io


# настройка веб-драйвера
def create_driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    # options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver

# ищем все статьи на Scopus
def find_all_articles(req):
    driver_request = create_driver()
    driver_request.get(f'https://www.scopus.com/results/results.uri?sid=a8ca21b3d6f1a6bbe11255d8e1fc1703&src=s&sot=b&sdt=b&origin=searchbasic&rr=&sl=18&s=TITLE-ABS-KEY({req})&searchterm1=%D0%B2%D0%B5%D0%B1&searchTerms=&connectors=&field1=TITLE_ABS_KEY&fields=')

    results = driver_request.find_elements_by_class_name('ddmDocTitle')

    urlArray = [] # ссылки на статьи
    for i in range(len(results)):
        url = results[i].get_attribute('href')
        urlArray.append(url)

    return urlArray

# чекаем статью и вытаскиваем всю необходимую информацию
def check_article(url):
    driver_article = create_driver()
    driver_article.get(url)

    time.sleep(2)

    # авторы
    dataAuthors = driver_article.find_elements_by_class_name('ul--horizontal')[0]
    string = dataAuthors.text

    authors = string.split(', ')
   
    # название статьи 
    title = driver_article.find_elements_by_class_name('Highlight-module__1p2SO')[0].text

    # ключевые слова
    key_words = []
    keys_span = driver_article.find_elements_by_xpath("//els-typography[@class='margin-size-8-r hydrated']")

    if len(keys_span) != 0:
        for i in range(len(keys_span)):
            key_words.append(keys_span[i].text)
    else: 
        key_words = "No key words"

    # источник
    source = driver_article.find_elements_by_tag_name('els-typography')[0].text
    

    # аннотация
    summary = driver_article.find_element_by_xpath("//els-typography[@indefinitewidthparagraph='true']").text
    

    info_about_article = {
        "article": url,
        "title": title,
        "authors": authors,
        "key words": key_words,
        "publication": source,
        "summary": summary
    }
    return info_about_article

# информация по всем найденным статьям
def get_articles(urls):

    all_information = []
    for index in range(len(urls)):

        info_article = check_article(articles_for_user[index])
        all_information.append(info_article)

    return all_information

# делаем запрос на Скопусе
start_time = time.time()
user_request = "веб"

articles_for_user = find_all_articles(user_request)
info = get_articles(articles_for_user)

# результаты парсинга записать в json
with io.open('articles_parser.json','w',encoding='utf-8') as f: 
    json.dump(info, f, indent=4, ensure_ascii=False)

print("--- %s seconds ---" % (time.time() - start_time))