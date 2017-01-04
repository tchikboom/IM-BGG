# -*- coding: utf-8 -*-

import re
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("ecriture", help="ERREUR")
parser.add_argument("lecture", help="ERREUR")
args = parser.parse_args()

tableau = open(args.ecriture, 'w', encoding="utf-8")
tableau.write('var table = `\n<HTML>\n<body>\n<div class="container">\n<section>\n<H4 ALIGN=CENTER><font color=000080><b>COMMENTAIRES</b></font color></H4>\n<table id="comments" class="display" cellspacing="0" width="100%">\n<thead> \n<tr> \n<th>Jeu</th> \n<th>id du jeu</th> \n<th>Note du joueur</th> \n<th>Localisation</th> \n<th>Commentaire</th> \n</tr> \n</thead> \n<tbody>\n')

with open(args.lecture, 'r', encoding="utf-8") as f:
	for line in f:	
		if re.search("note value=\"([^\"]*)\"", line):
			numero = re.search("note value=\"([^\"]*)\"", line)
			num = numero.group(1)

		if re.search("comment game=\"([^\"]*)", line):
			game = re.search("comment game=\"([^\"]*)", line)
			tableau.write("<tr>")
			tableau.write("<td>"+ game.group(1)+ "</td>")

		if re.search("game_id=\"([^\"]*)", line):
			game = re.search("game_id=\"([^\"]*)", line)
			tableau.write("<td>"+ game.group(1)+ "</td>\n<td>"+ num+ "</td>")

		if re.search("location=\"([^\"]*)", line):
			game = re.search("location=\"([^\"]*)", line)
			tableau.write("<td>"+ game.group(1)+ "</td>")

		if re.search("comment game=.*>([^<]*)", line):
			game = re.search("comment game=.*>(.*)</comment>", line)
			tableau.write("<td>"+ game.group(1)+ "</td></tr>")

	tableau.write('</tbody></table></section></div></body></HTML>`;')