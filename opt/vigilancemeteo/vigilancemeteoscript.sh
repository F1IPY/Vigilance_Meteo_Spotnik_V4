#!/bin/bash
# 

python /opt/vigilancemeteo/vigilancemeteoscript.py 78
sleep 2

FILE=/tmp/meteocouleur
COULEUR=`cat $FILE`
dt=$(date '+%d/%m/%Y %H:%M:%S');
echo $dt $COULEUR > /home/log/vigilancemeteo.log


if [ $COULEUR != "Vert" ]
then
	COULEUR=`cat $FILE`."wav"
	FILE1=/tmp/meteoalert
	ALERT=`cat $FILE1`."wav"
	echo $ALERT >> /home/log/vigilancemeteo.log
	sox /usr/share/svxlink/sounds/fr_FR/vigilance/f1ipy.wav  /usr/share/svxlink/sounds/fr_FR/vigilance/bulletin.wav /usr/share/svxlink/sounds/fr_FR/vigilance/alert.wav /usr/share/svxlink/sounds/fr_FR/vigilance/$COULEUR /usr/share/svxlink/sounds/fr_FR/vigilance/pour.wav /usr/share/svxlink/sounds/fr_FR/vigilance/$ALERT  -r 16000 -b 16 /usr/share/svxlink/sounds/fr_FR/RRF/f1ipy.wav
else
	sox /usr/share/svxlink/sounds/fr_FR/vigilance/f1ipy.wav -r 16000 -b 16 /usr/share/svxlink/sounds/fr_FR/RRF/f1ipy.wav

fi

