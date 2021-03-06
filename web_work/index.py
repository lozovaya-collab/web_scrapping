import io
import requests
import json
import time


SCOPUS_API_KEY = "b4e440e2a44b935746ed7eb2882eadaa"
scopus_articles_search_url = 'http://api.elsevier.com/content/search/scopus?'
headers = {'Accept':'application/json', 'X-ELS-APIKey': SCOPUS_API_KEY}
search_query = 'query=TITLE-ABS-KEY(веб)'

start_time = time.time()

scopus_request = requests.get(scopus_articles_search_url + search_query, headers=headers)
# print(page_request.url)

# response to json
page = json.loads(scopus_request.content.decode("utf-8"))
with io.open('ans.json','w',encoding='utf-8') as f: 
    json.dump(page["search-results"]["entry"], f, indent=4, ensure_ascii=False)

articles_API = page["search-results"]["entry"]


array_info = []  
    


for i in range(len(articles_API)):

    article = page["search-results"]["entry"][i]

    url_scopus_api = article["link"][2]["@href"]
    
    page_requst = requests.get(article["prism:url"], headers=headers)
    page_article = json.loads(page_requst.content.decode("utf-8"))

    with io.open('article.json','w',encoding='utf-8') as f: 
        json.dump(page_article, f, indent=4, ensure_ascii=False)
    
    article_info = page_article["abstracts-retrieval-response"]["item"]["bibrecord"]["head"]

    title_scopus_api = article_info["citation-title"]

    if isinstance(article_info["author-group"], list):
        authors = article_info["author-group"][0]["author"]
    else:
        authors = article_info["author-group"]["author"]
    
    authors_scopus_api = []

    for i in range(len(authors)):
        person = authors[i]["preferred-name"]
        authors_scopus_api.append(person["ce:given-name"] + " " + person["ce:surname"])

    key_words_scopus_api = []

    if "citation-info" in article_info:
        citation = article_info["citation-info"]
        if "author-keywords" in citation:
            for i in range(len(article_info["citation-info"]["author-keywords"]["author-keyword"])):
                key = article_info["citation-info"]["author-keywords"]["author-keyword"][i]["$"]
                key_words_scopus_api.append(key)
        else:
            key_words_scopus_api = "No key words"

    publication_scopus_api = page_article["abstracts-retrieval-response"]["coredata"]["prism:publicationName"]
    summary_scopus_api = article_info["abstracts"]

    info_about_article = {
        "article": url_scopus_api,
        "title": title_scopus_api,
        "authors": authors_scopus_api,
        "key words": key_words_scopus_api,
        "publication": publication_scopus_api,
        "summary": summary_scopus_api
    }

    array_info.append(info_about_article)

with io.open('articles_api.json','w',encoding='utf-8') as f: 
    json.dump(array_info, f, indent=4, ensure_ascii=False)

print("--- %s seconds ---" % (time.time() - start_time))