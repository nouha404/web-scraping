from bs4 import BeautifulSoup
import requests
from tinydb import TinyDB

db = TinyDB('All_pays.json', indent=4)
Pays = db.table('Pays')


def get_url():
    all_page = []
    array_content_name_page = []
    for page in range(25):
        pages = requests.get(f'http://example.python-scraping.com//places/default/index/{page}')
        soup = BeautifulSoup(pages.content, 'html.parser')

        if pages.status_code == 200:
            print(f'Chargement de {pages.url} ...')
            all_page.append(pages.url)

        # Gerer les lien qui ont les informations des pays
        for content_page in all_page:
            link_request = requests.get(content_page)
            link_soup = BeautifulSoup(link_request.content, 'html.parser')
            # On recupere le nom des pays afin d'aller chercher les infos dessus
            name_pays = link_soup.findAll('td')[0]

            # Iterer sur name_pays afin d'obtenir tout les nom des pays avec le deuxieme lien
            for name in name_pays.next_element.stripped_strings:
                for i in range(0, 25):
                    content_name_page = f'http://example.python-scraping.com/places/default/view/{name}-{i}'
                    array_content_name_page.append(content_name_page)

    # Recuperer les infos
    for content in array_content_name_page:
        links_request = requests.get(content)
        links_soup = BeautifulSoup(links_request.content, 'html.parser')
        population = links_soup.findAll('tr', id='places_population__row')
        country = links_soup.findAll('tr', id='places_country_or_district__row')
        capitale = links_soup.findAll('tr', id='places_capital__row')

        for ctr in country:
            for cap in capitale:
                # Refactoring avec u compression de list
                [Pays.insert_multiple([{
                    ctr.text: ctr.next_sibling.text,
                    cap.text: cap.next_sibling.text,
                    pop.text: pop.next_sibling.text}]) for pop in population]


get_url()
