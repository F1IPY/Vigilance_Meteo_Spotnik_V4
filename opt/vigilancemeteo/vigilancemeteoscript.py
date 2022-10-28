#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import vigilancemeteo


Dept=sys.argv[1]


print ( Dept )
zone = vigilancemeteo.DepartmentWeatherAlert(Dept)

couleur = zone.department_color
print ( couleur ) 
text = zone.summary_message('text')
print ( text )
fichier = open("/tmp/meteocouleur", "w")
fichier.write(couleur)
fichier.close()
fichier = open("/tmp/meteoalert", "w")
fichier.write(text)
fichier.close()

