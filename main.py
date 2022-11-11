'''
https://dadosabertos.tse.jus.br/dataset/resultados-2022-boletim-de-urna

https://dadosabertos.tse.jus.br/dataset/resultados-2022-boletim-de-urna/resource/fdaba499-49eb-4bf7-be53-b34254efa38b

https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/bweb_1t_AC_051020221321.zip

ul class="resource-list"
li
'''
import time
import requests
import os
import urllib.request
from bs4 import BeautifulSoup
from os.path import basename
from urllib.parse import urlsplit
from os.path import exists


URL = 'https://dadosabertos.tse.jus.br'
URL_PATH = '/dataset/resultados-2022-boletim-de-urna'
DIR_NAME = 'downloads/'


def url2name(url):
    return basename(urlsplit(url)[2])


def download(url):
    localName = url2name(url)
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req)

    if os.path.isfile(localName):
        print('Já foi baixado o arquivo {}'.format(localName))
    else:
        print('Baixando o arquivo {}'.format(localName))

    localName = os.path.join(DIR_NAME, localName)

    f = open(localName, 'wb')
    f.write(r.read())
    f.close()


def get_links_from():
    links = []
    r = requests.get('{}{}'.format(URL, URL_PATH))
    if r.status_code != 200:
        return None
 
    soup = BeautifulSoup(r.content, 'html.parser')

    for li in soup.findAll('li', attrs={'class': 'resource-item'}):
        links.append(li.find('a').get('href'))
    return links


def download_files():
    for file in get_links_from():
        url = '{}{}'.format(URL, file)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        download_url = soup.find('a', attrs={'class': 'resource-url-analytics'}).get('href')
        download(download_url)

        time.sleep(5)


if __name__ == "__main__":
    download_files()