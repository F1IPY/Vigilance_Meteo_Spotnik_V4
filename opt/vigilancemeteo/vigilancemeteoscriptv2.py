import requests
import sys

API_KEY = "votre API key"
URL = "https://public-api.meteofrance.fr/public/DPVigilance/v1/cartevigilance/encours"

COLORS = {
    1: "VERT",
    2: "JAUNE",
    3: "ORANGE",
    4: "ROUGE"
}

# VIGILANCE_TYPES = {
#     1: "VENT",
#     2: "PLUIE",
#     3: "ORAGES",
#     4: "CRUES",
#     5: "NEIGE_VERGLAS",
#     6: "CANICULE",
#     7: "GRAND_FROID",
#     8: "AVALANCHES",
#     9: "VAGUES_SUBMERSION",
# }

def get_vigilance(dep):
    headers = {"apikey": API_KEY}

    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()

    data = r.json()

    # Période J
    domains = data["product"]["periods"][0]["timelaps"]["domain_ids"]

    for domain in domains:

        if domain["domain_id"] == str(dep).zfill(2):

            couleur_max = COLORS[domain["max_color_id"]]

            # Recherche du phénomène le plus sévère
            best_type = 0
            best_color = 0

            for ph in domain["phenomenon_items"]:

                pid = int(ph["phenomenon_id"])
                color = int(ph["phenomenon_max_color_id"])

                if color > best_color:
                    best_color = color
                    best_type = pid

            return couleur_max, best_type

    return None, None


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage : vigilance3.py <departement>")
        sys.exit(1)

    couleur, type_vigilance = get_vigilance(sys.argv[1])

    if couleur is None:
        print("ERREUR")
    else:
        print(f"{couleur};{type_vigilance}")