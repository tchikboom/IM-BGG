#!/usr/bin/python
# coding: utf8

"""
    NAME
        opinion2wordcloud.py

    SYNOPSIS
        python3 extraction_bgg.py

    DESCRIPTION
        A partir des résultats de l'extraction d'opinion des commentaires
        du site BoardGameGeek, crée des fichiers pour pouvoir créer des nuages
        de mots.

        Fichier d'entrée:
            opinion.json : Résultats de l'extraction d'opinion, au format suivant :
                                "MOT" : [score_positif, score_négatif, score_neutre]

        Fichiers de sortie :
            positif/negatif_wordcloud.txt : Fichier texte contenant les mots
                                            les plus positifs ou les plus négatifs.
            Puisque Wordle, le service de nuage de mots que l'on
            souhaite utiliser, prend en entrée des textes bruts et compte la
            fréquence de chaque mot pour créer le nuage, nos fichiers de sortie
            contiennent X fois chaque mot pertinent, où X est le score positif
            ou négatif du mot.
"""

import json
from operator import itemgetter


def main():
    with open("opinions.json", "r") as o:
        j = json.load(o)

    # Pour chaque mot du fichier de résultats, on le stocke avec son score
    # de polarité dans la liste de tuple correspondant.
    positif = list()
    negatif = list()

    for mot in j:
        score_pos = j[mot][0]
        score_neg = j[mot][1]

        positif.append((mot, score_pos))
        negatif.append((mot, score_neg))

    # On trie les données en ordre décroissant pour récupérer les mots
    # les plus positifs ou négatifs.
    positif.sort(key=itemgetter(1), reverse=True)
    negatif.sort(key=itemgetter(1), reverse=True)

    # Ecriture des fichiers de sortie
    # Ecrit X fois chaque mot dans le fichier, où X est le score de polarité du mot
    with open("positif_wordcould.txt", "w") as pos_output:
        for tup in positif[0:20]:
            i = 0
            mot = tup[0]
            score = int(tup[1])
            while i < score:
                pos_output.write(mot + " ")
                i += 1

    with open("negatif_wordcould.txt", "w") as neg_output:
        for tup in negatif[0:20]:
            i = 0
            mot = tup[0]
            score = int(tup[1])
            while i < score:
                neg_output.write(mot + " ")
                i += 1


if __name__ == '__main__':
    main()
