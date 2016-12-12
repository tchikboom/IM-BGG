#!/usr/bin/python
# coding: utf8

from lxml import etree
import math
import time
import progressbar
from bs4 import BeautifulSoup
import re
import urllib.request


def request_builder(start):
    """
    Construit l'URL nécessaire pour la requête GET
        id = 1,2,3... : jeux à récupérer
                        (par blocs de 32 à cause de restrictions de l'API)
        comments=1 > fait apparaître les commentaires sur le jeu avec leur note
        stats=1 > fait apparaître les stats du jeu, (poids, note pondérée...)
        pagesize=100 > fait apparaître le plus grand nombre de commentaires
    """
    request = 'http://boardgamegeek.com/xmlapi2/thing?id='
    end = start + 31
    while start < end:
        request = request + str(start) + ','
        start += 1

    request = request + str(end) + '&comments=1&stats=1&pagesize=100'
    return request


def hot_list(end):
    """
    Construit une liste d'id en fonction des jeux populaires sur BGG
    int end : dernière page du parsing, 50 jeux par page
    """
    i = 1
    list_id = []

    while i <= end:
        url = "http://boardgamegeek.com/browse/boardgame/page/" + str(i)
        # GET de la page hot
        doc = urllib.request.urlopen(url).read()
        # Parsing de la page
        page = BeautifulSoup(doc, 'lxml')
        # table des hot items
        table = page.find(id="collectionitems")
        # td qui contient entre autres le lien du jeu
        for td in table.find_all("td", class_="collection_thumbnail"):
            # lien du jeu
            a = td.find('a')
            link = a['href']
            # Récupération de l'id
            re_id = re.search("[0-9]+", link)
            id_jeu = re_id.group()
            list_id.append(id_jeu)
        i += 1
        # Sleep de 5 secondes pour respecter les restrictions de BGG
        if end != 1:
            time.sleep(5)
    return list_id

# Ouverture d'un fichier où on stocke les noms d'utilisateurs
usernames = open("usernames.txt", 'w')

# Création d'une structure XML où on stocke les commentaires triés par note
xml_coms = etree.Element("comments")

# Création des éléments "notes", de 0 à 10
for i in range(11):
    note = etree.SubElement(xml_coms, "note")
    note.set("value", str(i))

compteur_jeux = 1
max_jeux = 100

# Barre de progression, fancy!
bar = progressbar.ProgressBar(max_value=max_jeux)

# Boucle de parsing sur BGG
while compteur_jeux < max_jeux:
    request = request_builder(compteur_jeux)
    # Parsing XML des infos d'une série de jeux
    xml_in = etree.parse(request)
    bar.update(compteur_jeux)

    # Boucle sur chaque commentaire
    for comment in xml_in.xpath("/items/item/comments/comment"):
        rating = comment.get('rating')
        # On veut un int comme note pour pouvoir trier les coms par note
        if rating == "N/A":
            continue
        try:
            rating = int(rating)
        except ValueError as e:
            # S'il y a toujours une ValueError, alors rating est un float
            rating = float(rating)
            rating = math.floor(rating)

        content = comment.get('value')
        user = comment.get('username')

        # Stockage des résultats
        com = etree.SubElement(xml_coms[rating], "comment")
        com.text = comment.get('value')
        usernames.write(user + '\n')

    compteur_jeux += 32

    # On attend 5 secondes pour respecter les conditions d'utilisation
    time.sleep(5)

bar.update(max_jeux)
print('\n', end="")

# Impression de la structure xml
et = etree.ElementTree(xml_coms)
et.write("comments.xml", xml_declaration=True, pretty_print=True)