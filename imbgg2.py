#!/usr/bin/python
# coding: utf8

from lxml import etree
import math
import time
import progressbar
from bs4 import BeautifulSoup
import re
import urllib.request


def hot_list(page):
    """
    Construit une liste d'id en fonction des jeux populaires sur BGG
    page : numéro de page de la hotlist à parser, 50 jeux / page
    """
    list_id = []

    url = "http://boardgamegeek.com/browse/boardgame/page/" + str(page)
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
    return list_id

def request_builder(id):
    requete = "http://boardgamegeek.com/xmlapi2/thing?id="
    requete = requete + str(id)
    requete = requete + "&comments=1&stats=1&pagesize=100"
    return requete

# Création d'une structure XML où on stocke les commentaires triés par note
xml_coms = etree.Element("comments")

# Création des éléments "notes", de 0 à 10
for i in range(11):
    note = etree.SubElement(xml_coms, "note")
    note.set("value", str(i))

# Barre de progression, fancy!
bar = progressbar.ProgressBar(max_value=50)
bar.update(0)
hotlist = hot_list(1)
i = 0
# Boucle de parsing sur BGG
for id in hotlist[0:50]:
    request = request_builder(id)
    # Parsing XML des infos d'une série de jeux
    xml_in = etree.parse(request)

    #Récupération du nom du jeu et de son id
    name = xml_in.xpath('/items/item/name[@type="primary"]/@value')[0]
    id_jeu = xml_in.xpath('/items/item/@id')[0]

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
            # Arrondit la note à l'entier inférieur
            rating = math.floor(rating)

        # Contenu du comment
        content = comment.get('value')

        # Récupération des stats
        avg_rating    = xml_in.xpath("/items/item/statistics/ratings/bayesaverage")[0].get("value")
        minplayers    = xml_in.xpath("/items/item/minplayers")[0].get("value")
        maxplayers    = xml_in.xpath("/items/item/maxplayers")[0].get("value")
        playing_time  = xml_in.xpath("/items/item/playingtime")[0].get("value")
        minage        = xml_in.xpath("/items/item/minage")[0].get("value")
        weight        = xml_in.xpath("/items/item/statistics/ratings/averageweight")[0].get("value")
        gamemechanics = []
        for mech in xml_in.xpath("/items/item/link[@type='boardgamemechanic']"):
            gamemechanics.append(mech.get("value"))

        # Récupération du pays de chaque user
        user = comment.get('username')
        user_profile = str("http://www.boardgamegeek.com/xmlapi2/user?name=" + user)
        xml_user = etree.parse(user_profile)
        location= xml_user.xpath("/user/country")
        country = location[0].get('value')
        time.sleep(5)

        # Stockage des infos des commentaires
        com = etree.SubElement(xml_coms[rating], "comment")
        com.text = comment.get('value')
        com.set("game", name)
        com.set("game_id", id_jeu)
        com.set("location", country)

        # Stockage des informations des stats
        xml_stats  = etree.Element("stats")
        jeu        = etree.SubElement(xml_stats, "jeu")
        nom        = etree.SubElement(jeu, "nom")
        moyenne    = etree.SubElement(jeu, "moyenne")
        nb_joueurs = etree.SubElement(jeu, "nb_joueurs")
        min_j      = etree.SubElement(nb_joueurs, "min")
        max_j      = etree.SubElement(nb_joueurs, "max")
        tps_jeu    = etree.SubElement(jeu, "temps_jeu")
        age_min    = etree.SubElement(jeu, "age_minimum")
        complexite = etree.SubElement(jeu, "complexite")
        mecaniques = etree.SubElement(jeu, "mecaniques")

        jeu.set("id", id_jeu)
        nom.set("value", name)
        moyenne.set("value", avg_rating)
        min_j.set("value", minplayers)
        max_j.set("value", maxplayers)
        tps_jeu.set("value", playing_time)
        age_min.set("value", minage)
        complexite.set("value", weight)
        for mech in gamemechanics:
            meca = etree.SubElement(mecaniques, "mecanique")
            meca.set("value", mech)
    i += 1
    bar.update(i)
     # On attend 5 secondes pour respecter les conditions d'utilisation
    time.sleep(5)

bar.update(50)
print('')

# Impression de la structure xml
et1  = etree.ElementTree(xml_coms)
et2 = etree.ElementTree(xml_stats)
et1.write("comments.xml", xml_declaration=True, pretty_print=True)
et2.write("stats.xml", xml_declaration=True, pretty_print=True)
