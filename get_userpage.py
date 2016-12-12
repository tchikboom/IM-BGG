#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
br = mechanize.Browser()
br.set_handle_robots(False)

users =["passager57","79strat","dfwilkinson","coolmew","Paragonical","passager57","cbclimber","GodHand","Phija","shaggi30","Eyeballguy","emodiu5","charlest","jtdubya","Jasonhofstedt","realkenzaburo","Dafonzi81","windmastermanwe","danom","orabbi","Darkpixel","sever2morrow","cdngka","icechamber","terrydactyl","CamT","MightyCamel","Zakoholic","TylerGoble1","AndrewAU","Frohike","AgentDib","alvinsimms","doidospordados","malmby","Burnham","RickyKarnage","momper","Hoju22", "Anteros311"]


	
################	
#DL les fichiers XML
################
"""	
for user in users:
	user = user.strip()
	lien = str("https://www.boardgamegeek.com/xmlapi2/user?name=" + user)
	fich = str(user + ".xml")
	br.open(lien)
	br.retrieve(lien, fich)
"""

################		
"""
Stocke le contenu de la page xml dans fiche_user
Peut être utilisé comme variable pour regexer dessus
Peut-être parsé par lxml ??? A vérifier
"""
for user in users:
	lien = str("https://www.boardgamegeek.com/xmlapi2/user?name=" + user)
	fich = str(user + ".xml")
	br.open(lien)
	fiche_user = br.response().read()

