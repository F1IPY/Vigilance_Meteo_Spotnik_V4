# Vigilance_Meteo_Spotnik_V4
 Vigilance Météo sur Spotnik V4
 
 Je vous partage  l'intégration de la diffusion d'un message de vigilance météo sur Sponik V4.

Je me suis inspiré de l'article de Frédéric (F4IJC) sur le site Vigilance météo & svxlink – F6KEX. La solution qu'il propose n'étant pas particulièrement adaptée pour un Spotnik, j'ai cherché une autre manière de faire.

Attention:
Cette manipulation doit être effectuée par les OM ayant un minimum de connaissance sur Linux !
Ne pas oublier de faire une sauvegarde de votre installation avant toute modification
L'intégration a été faite sur une version Spotnik V4 F8ASB (usvxcard) uniquement.

Vigilance Météo sur spotnik V4

Mise à jour du Spotnik
Commençons par mettre à jour le système. Cette étape est indispensable pour la suite:
Connexion en SSH sur le spotnik en Root
Tapez les commandes suivantes:
apt-get update --allow-releaseinfo-change
apt-get upgrade

Installation du package VigilanceMeteo (disponible sur GitHub: https://github.com/oncleben31/vigilancemeteo)
installer les dépendances
Tapez les commandes suivantes:
apt-get install libxslt1.1
apt-get install libxslt1-dev
apt-get install libxml2
apt-get install libxml2-dev

Puis les scripts python
python -m pip install vigilancemeteo

Creation du fichier Python
Nous allons maintenant créer le script qui va nous permettre de vérifier le fonctionnement
Creer un répertoire vigilancemeteo dans opt:

cd /
cd opt
mkdir vigilancemeteo
cd vigilancemeteo

copier le fichier vigilancemeteoscript.py adns le répertoire

rendre le fichier exécutable:
chmod 755 vigilancemeteoscript.py

Si toutes les opérations ci dessus ont été effectué correctement vous pouvez enfin tester le script en tapant la commande:
Pour le département 78
python  vigilancemeteoscript.py 78

Vous devez voir à l'écran la réponse:
root@uSvxCardV4:/opt/vigilancemeteo# python vigilancemeteoscript.py 78
78
Vert
Aucune alerte météo en cours.

pour le département 64
root@uSvxCardV4:/opt/vigilancemeteo# python vigilancemeteoscript.py 64
64
Jaune
Alerte météo Jaune en cours :
 - Avalanches: Jaune

Modification du script python original
Le format du texte retourné n'étant pas approprié pour notre utilisation nous allons devoir modifier le fichier suivant
nano /usr/local/lib/python2.7/dist-packages/vigilancemeteo/department_weather_alert.py

aux lignes 126 à 133:

<code>
                 message = "Alerte météo {} en cours :".format(self.department_color)
                # Order the dictionary keys because before python 3.6 keys are
                # not ordered
                for type_risque in sorted(self.alerts_list.keys()):
                    if self.alerts_list[type_risque] != "Vert":
                        message = message + "\n - {}: {}".format(
                            type_risque, self.alerts_list[type_risque]
                        )
</code>

 remplacez les par
 
<code>
        # message = "Alerte météo {} en cours :".format(self.department_color)
                # Order the dictionary keys because before python 3.6 keys are
                # not ordered
                for type_risque in sorted(self.alerts_list.keys()):
                    if self.alerts_list[type_risque] != "Vert":
                        message = format(
                           type_risque
                        )
</code>

Ce qui va avoir pour effet de modifier la sortie texte avec uniquement les informations utiles.
Ce qui donne pour le département 64:
root@uSvxCardV4:/opt/vigilancemeteo# python vigilancemeteoscript.py 64
64
Jaune
Avalanches


Creation des fichiers audio
Nous devons créer un nouveau répertoire pour les fichiers audio de la vigilance météo:
mkdir /usr/share/svxlink/sounds/fr_FR/vigilance
et y mettre les fichiers audio 

Et pour finir le fichier qui correspond à l'annonce de votre HotSpot
sftp://root@....11/usr/share/svxlink/sounds/fr_FR/vigilance/ShortAnnonce.wav

Pour créer les fichiers audio j'utilise Amazon Polly qui est gratuit pendant un an sur la plateforme AWS.

Création du fichier shell vigilancemeteoscript.sh
Ce script permet de récupérer les informations de vigilance et de concaténer les fichiers audio pour créer l'annonce finale.
cd /
cd opt
cd vigilancemeteo

créer le fichier vigilancemeteoscript.sh


Courage nous y sommes presque...
Exécution automatique du script
Il faut maintenant exécuter ce fichier de manière automatique toutes les heures.
pour ce faire nous ajoutons la ligne suivante dans le fichier crontab:
nano /etc/crontab

## Vigilance Météo
00 0-23 * * * root /opt/vigilancemeteo/vigilancemeteoscript.sh
Activation de l'annonce
J'ai fais le choix d'annoncer la vigilance météo (uniquement quand il y en a une) toutes les 30 minutes
Il faut donc activer l'annonce "short annonce" du HotSpot dans le fichier svxlink.cfg

nano /etc/spotnik/svxlink.cfg
Dans la section  [SimplexLogic]
 SHORT_IDENT_INTERVAL=30

Et indiquer le nom du fichier dans le fichier Logic.tcl
nano /usr/share/svxlink/events.d/local/Logic.tcl
variable short_announce_file    "/usr/share/svxlink/sounds/fr_FR/RRF/ShortAnnonce.wav";

Maintenant écouter votre hotspot !

Je ne suis pas un expert Linux et encore moins pour le shell et python, je suis donc convaincu que les scripts proposés peuvent être améliorés/ optimisés. Ceci dit, cette configuration fonctionne chez moi depuis plusieurs mois.

73

Christophe (F1IPY)
