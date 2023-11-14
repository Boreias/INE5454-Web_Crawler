import requests # para requisições http
import json # para gerar JSON a partir de objetos do Python
from bs4 import BeautifulSoup # BeautifulSoup é uma biblioteca Python de extração de dados de arquivos HTML e XML.
import re
import time
from sports import popular_sports

# Press the green button in the gutter to run the script.

def analisaSite(site_analisado, lista_resultados, headers):
    try:
        requisicaoDePagina = requests.get(site_analisado, headers=headers)

        conteudo = requisicaoDePagina.content

        site = BeautifulSoup(conteudo, 'html.parser', from_encoding='iso-8859-1')

        esporte = site.find_all('h3')


        pattern = r'(\d+)[\s\W]*(' + '|'.join(map(re.escape, popular_sports)) + r')\b'

        comp = re.compile(pattern, re.IGNORECASE)

        lista_sports_do_site = []

        for i in esporte:
            matches = re.findall(comp, str(i))
            if (len(matches) > 0):
                lista_sports_do_site.append(matches[0])

        if len(lista_sports_do_site) > 2:
            lista_resultados[site_analisado] = lista_sports_do_site

        sites_filhos = [a.get('href') for a in site.find_all('a') if a.get('href') and a.get('href').startswith('http')]

        j = 0

        while j < len(sites_filhos):

            if sites_filhos[j] in lista_resultados.keys() or sites_filhos[j].find(' ') > 0 or sites_filhos[j].find('.com') < 0:
                sites_filhos.pop(j)
                j -= 1
            j += 1

        return sites_filhos

    except requests.exceptions.RequestException:
        return []


if __name__ == '__main__':
    tempo_inicial = time.time()
    lista_sites_mundo = ['https://sportsmonkie.com/most-popular-sports/',
                         'https://www.thetealmango.com/sports/most-popular-sport-in-the-world/',
                         'https://sportytell.com/sports/most-popular-sports-world/']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'}
    lista_resultados = dict()

    sites_pais = lista_sites_mundo

    try:

        while True:
            sites_filhos = []

            for site_analisado in sites_pais:

                sites_filhos += analisaSite(site_analisado, lista_resultados, headers)

            sites_pais = sites_filhos

    except:
        tempo_final = time.time()
        print('O tempo de processamento foi de ' + str((tempo_final - tempo_inicial)//1) + ' segundos')
        print(lista_resultados)


