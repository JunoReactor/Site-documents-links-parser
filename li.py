from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import urlparse
from requests_html import HTMLSession
import urllib.request
import re
import os
import urllib
import colorama
import requests
import validators
import time
 
urlsCrawl           = list()
internal_link       = list()
internal_file_link  = list()
external_link       = list()
internal_400_link   = list()
internal_404_link   = list()
internal_302_link   = list()
internal_303_link   = list()
internal_401_link   = list()
internal_502_link   = list()
internal_error_link   = list()
headers             = ["application/force-download","application/x-compress","application/x-gzip","application/x-zip","application/zip","application/x-tiff","application/tiff","application/compact_pro","application/tif","application/x-tif","image/tif","image/x-tif","image/x-tiff","application/pdf","application/msword","application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/vnd.openxmlformats-officedocument.wordprocessingml.template","application/vnd.ms-word.document.macroEnabled.12","application/vnd.ms-word.template.macroEnabled.12","image/jpeg","video/mp4","image/png","application/vnd.openxmlformats-officedocument.presentationml.presentation","application/vnd.ms-excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","application/zip","image/jpg","application/x-7z-compressed","application/vnd.rar","application/x-rar-compressed","application/octet-stream","application/zip, application/octet-stream", "application/x-zip-compressed", "multipart/x-zip","application/rtf","application/vnd.ms-powerpoint","video/mp4","audio/mpeg","image/gif","application/gzip","text/csv","audio/aac"]
limit = 5
i = 1

GREEN   = colorama.Fore.GREEN
GRAY    = colorama.Fore.LIGHTBLACK_EX
WHITE   = colorama.Fore.WHITE
RESET   = colorama.Fore.RESET
YELLOW  = colorama.Fore.YELLOW
RED     = colorama.Fore.RED
CYAN    = colorama.Fore.CYAN

def crawl(urlopen):
    global urlsCrawl
    global baseURL
    global internal_file_link
    global internal_link
    global max_urls
    global internal_400_link
    global internal_404_link
    global internal_302_link
    global internal_303_link
    global internal_401_link
    global internal_502_link
    global internal_error_link
    global i
    global headers
    global sleep
    
    if max_urls != 0:
        if i > max_urls:
            return

    urlsPage = list()
    urlopen = urlopen.strip()

    if urlopen=='#':
        return

    urlopen = urlopen.replace(" ", "%20")

    # Парсим URL 
    purlopen = urlparse(urlopen)

    if purlopen.netloc=='' and purlopen.path=='' or purlopen.scheme=='mailto' or purlopen.scheme=='tel' or purlopen.scheme=='fax':
        return

    if purlopen.path=='/':
        urlopen = baseURL

    # Если текущего URL нет в глобальном массиве урлов, то добавляем его
    if urlopen in urlsCrawl:
        #print ('True...'+urlopen)
        return
    else:
        #print ('False...'+urlopen)
        urlsCrawl.append(urlopen)

    # Проверяем коды ответов
    try:
        if purlopen.netloc=='' and baseURL != urlopen:
            if urlopen[0] != '/':
                urlopen = "/"+urlopen
            requrl = baseURL+urlopen
        else:
            requrl = urlopen

        if not validators.url(requrl):
            return
        else:    
            r = requests.head(requrl, allow_redirects=True)
            if r.status_code == 303:
                internal_303_link.append(requrl)
                return
            if r.status_code == 302:
                internal_302_link.append(requrl)
                return
            if r.status_code == 401:
                internal_401_link.append(requrl)
                return
            if r.status_code == 400:
                internal_400_link.append(requrl)
                return
            if r.status_code == 502:
                internal_502_link.append(requrl)
                return
            if r.status_code == 404:
                internal_404_link.append(requrl)
            if r.status_code == 200:
                if r.headers['Content-Type'] in headers:
                    internal_file_link.append(urlopen.replace("%20", " "))
                    print(f"{GREEN}[*] Документ: {requrl}{RESET}")
                    return
            else:
                return

    except requests.ConnectionError:
        print(f"{RED}[*] Ошибка подключения: {requrl}{RESET}")
        internal_error_link.append(requrl)
        return

    # Делаем запрос к странице
    try:
        html_page = urllib.request.urlopen(requrl)
    except UnicodeEncodeError:
        print(f"{RED}[*] URL не валидный для парсинга: {requrl}{RESET}")
        internal_error_link.append(requrl)
        return
    except UnicodeDecodeError:
        print(f"{RED}[*] URL не валидный для парсинга: {requrl}{RESET}")
        internal_error_link.append(requrl)
        return 
    except urllib.error.HTTPError:
        print(f"{RED}[*] URL не валидный для парсинга: {requrl}{RESET}")
        internal_error_link.append(requrl)
        return
    except urllib.error.URLError:
        print(f"{RED}[*] URL не валидный для парсинга: {requrl}{RESET}")
        internal_error_link.append(requrl)
        return 
    except ValueError:
        print(f"{RED}[*] URL не валидный для парсинга: {requrl}{RESET}")
        internal_error_link.append(requrl)
        return
    
    print(f"{YELLOW}[*] Проверяется: {requrl}{RESET}")
    internal_link.append(requrl.replace("%20", " "))
    i=i+1

    # Парсим страницу
    soup = BeautifulSoup(html_page, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")

        # Добавляем в массив urlsPage если их там нет
        if href not in urlsPage:
            urlp = urlparse(href)
            if urlp.netloc=='':
                urlsPage.append(href)
            elif urlp.netloc=='old.sibur.ru':
                urlsPage.append(href)
    
    urlsPage.sort()

    # Проходим по urlsPage
    for url in urlsPage:
        if url not in urlsCrawl:
            time.sleep(sleep)
            crawl(url.strip())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="URL адрес для извлечения ссылок")
    parser.add_argument("-m", "--max-urls", help="Максимальное число для обхода, по умолчанию 30, 0 - без ограничений", default=30, type=int)
    parser.add_argument("-s", "--sleep", help="Таймаут для каждой итерации сек, по умолчанию 0.", default=0, type=float)
    
    args        = parser.parse_args()
    urlopen     = args.url
    max_urls    = args.max_urls
    sleep       = args.sleep

    purlparse = urlparse(urlopen)
    domain_name = purlparse.netloc
    baseURL = purlparse.scheme+'://'+purlparse.netloc

    crawl(urlopen)

    # Сохраняем
    with open(f"{domain_name}_internal_file_link.txt", "w") as f:
        for link in internal_file_link:
            print(link.strip(), file=f)

    # Сохраняем
    with open(f"{domain_name}_internal_link.txt", "w") as f:
        for link in internal_link:
            print(link.strip(), file=f)

    # Сохраняем
    with open(f"{domain_name}_internal_302_link.txt", "w") as f:
        for link in internal_302_link:
            print(link.strip(), file=f)

    # Сохраняем
    with open(f"{domain_name}_internal_303_link.txt", "w") as f:
        for link in internal_303_link:
            print(link.strip(), file=f)

    # Сохраняем
    with open(f"{domain_name}_internal_401_link.txt", "w") as f:
        for link in internal_401_link:
            print(link.strip(), file=f)

    # Сохраняем
    with open(f"{domain_name}_internal_404_link.txt", "w") as f:
        for link in internal_404_link:
            print(link.strip(), file=f)

    # Сохраняем
    with open(f"{domain_name}_internal_502_link.txt", "w") as f:
        for link in internal_502_link:
            print(link.strip(), file=f) 

    print(f"{GRAY}#################################################{RESET}")
    print(f"{CYAN}[*] Обработано внутренних URL адресов: {len(internal_link)}{RESET}")
    print(f"{CYAN}[*] Обработано URL файлов: {len(internal_file_link)}{RESET}")
    print(f"{CYAN}[*] Обработано URL 303: {len(internal_302_link)}{RESET}")
    print(f"{CYAN}[*] Обработано URL 302: {len(internal_303_link)}{RESET}")
    print(f"{CYAN}[*] Обработано URL 401: {len(internal_401_link)}{RESET}")
    print(f"{CYAN}[*] Обработано URL 404: {len(internal_404_link)}{RESET}")
    print(f"{CYAN}[*] Обработано URL 502: {len(internal_502_link)}{RESET}")
    print(f"{CYAN}[*] Суммарно URL обработано: {len(internal_link) + len(internal_file_link) + len(internal_302_link) + len(internal_303_link) + len(internal_401_link) + len(internal_404_link) + len(internal_502_link)}{RESET}")
    print(f"{GRAY}#################################################{RESET}")
