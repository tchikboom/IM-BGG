#!/usr/bin/python

from lxml import etree

def request_builder(start):
	"""
	Construit l'URL nécessaire pour la requête GET
		id = 1,2,3... : jeux à récupérer (par blocs de 32 pour restrictions techniques au niveau de l'API)
		comments > fait apparaître les commentaires sur le jeu avec leur note
		pagesize=100 > fait apparaître le plus grand nombre de commentaires (pas exactement 100)
	"""
	request = 'http://boardgamegeek.com/xmlapi2/thing?id='
	end = start + 31
	while start < end:
		request = request + str(start) + ',' 
		start += 1

	request = request + str(end) + '&comments=1&pagesize=100'
	return request

i = 1	# ID de début du parsing
j = 70	# ID de fin du parsing (arbitraire pour le moment)

# Création d'une structure XML
jeux = etree.Element("jeux")	# "jeux" est la racine

# Boucle de parsing sur BGG
# TODO : Ralentir les requêtes à 1 req / 5 sec.
while i <= j:
	request = request_builder(i)

	# Fait la requête GET et parse directement le XML obtenu
	xml = etree.parse(request)

	# Exemple de requête Xpath : print dans le stdout le nom anglais de chaque jeu
	for item in xml.xpath("/items/item/name[@type='primary']"):
		print(item.get('value'))

	# Exemple d'alimentaton du XML
	cpt = i
	#
	for item in xml.xpath("/items/item/name[@type='primary']"):
		jeu = etree.SubElement(jeux,"jeu") 	# <jeu> est child de <jeux>
		jeu.set("id",str(cpt)) 				# chaque jeu a un numéro d'id en attribut /!\ prend seulement des strings comme argument
		nom = etree.SubElement(jeu,"nom") 	# <nom> est child de <jeu>
		nom.text = item.get('value') 		# chaque jeu a une balise <nom>
		cpt += 1
	i += 32

# Impression de la structure XML dans un fichier
# TODO : Faire fonctionner pretty_print
fic = open("./premier_jet.xml",'w')
print(etree.tostring(jeux,pretty_print=True), end = "", file=fic)