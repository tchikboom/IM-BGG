<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method='html'/>
	<xsl:template match="stats">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>
Statistiques par jeu
</title>
</head>
<body>
	<table border="1px">
		<thead> 
			<tr> 
				<th>Id du jeu</th> 
				<th>Nom</th> 
				<th>Moyenne</th> 
				<th>Nb de joueurs(min)</th>
				<th>Nb de joueurs(max)</th> 
				<th>Temps de jeu</th>
				<th>Age minimum</th>
				<th>Complexité</th>
				<th>Mécaniques</th> 
			</tr> 
		</thead> 
		<tbody>
			<xsl:for-each select="jeu">
				<xsl:sort select="./moyenne/@value" order="descending" />
		      	<tr>
				<td><xsl:value-of select="@id" /></td>
		      	<td><xsl:value-of select="./nom/@value" /></td>
				<td><xsl:value-of select="./moyenne/@value" /></td>
				<td><xsl:value-of select="./nb_joueurs/min/@value" /></td>
		      	<td><xsl:value-of select="./nb_joueurs/max/@value" /></td>
	      		<td><xsl:value-of select="./temps_jeu/@value" /></td>
				<td><xsl:value-of select="./age_minimum/@value" /></td>
				<td><xsl:value-of select="./complexite/@value" /></td>
				<td><br/>
				<xsl:for-each select="./mecaniques/mecanique">
					<xsl:value-of select="@value" /><br/>
				</xsl:for-each>
				</td>	
		      	</tr>
			</xsl:for-each>
		</tbody>
    </table>
</body>
	</html>
	</xsl:template>
</xsl:stylesheet>


