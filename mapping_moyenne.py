#!/usr/bin/python
# coding: utf8

from lxml import etree
import math
import time
import progressbar
from bs4 import BeautifulSoup
import re
import urllib.request
import numpy

#Crée un dictionnaire Pays : code_iso
countriso = {}
with open("countries_iso.txt", 'r') as liste: #codes et pays telqu'utilisé par jvectormap
	for line in liste:
		line = line.strip()
		(iso, country) = line.split('\t')
		countriso[country] = iso
#print(countriso)

#Récupère toute les notes pour les pays dans countriso et calcul d'une moyenne par pays
#L'écrit dans le fichier javascript qui les matchera à la carte
#Possibilité de le faire dans le script qui scrappe???
v = open("moyenne.js", 'w')
v.write('var moyenne = {')
with open("comments_catan.xml", 'r') as fichier:
	prout = etree.parse(fichier)
	for country in countriso:
		coms = prout.xpath('/comments/note/comment[@location="'+country+'"]')
		notes = []
		for com in coms:
			note = com.xpath('../@value')
			notes.extend(note)
		notes = numpy.array(notes).astype(numpy.float) #le type de retour de lxml est "flexible", conversion nécessaire
		moyenne = round(numpy.mean(notes), 2)#arrondi 2 chiffre après la virgule
		if numpy.isnan(moyenne):#s'il n'y a pas de données, la moyenne est NaN, donc on l'ignore
			continue
		print (moyenne)
		
		v.write(countriso[country])
		v.write(' : ')
		v.write(str(moyenne))
		v.write(',\n')
	v.write('};')
	
