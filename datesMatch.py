import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

# Liste des URLs à traiter
urls = [
    "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2025/2026&codent=PTPL72&poule=DMG",
    "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2025/2026&codent=PTPL72&poule=DMF",
    "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2025/2026&codent=PTPL72&poule=CL6"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

matchs = []
aujourdhui = datetime.now().date()

# Boucle sur chaque URL
for url in urls:
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Déterminer la catégorie (Masculin, Féminin ou Loisir) via l'URL pour le JSON
        if "poule=DMG" in url:
            categorie = "Masculin"
        elif "poule=DMF" in url:
            categorie = "Féminin"
        else:   
            categorie = "Loisir"
        
        for ligne in soup.find_all("tr"):
            colonnes = ligne.find_all("td")
            
            # Filtre structure
            if len(colonnes) < 10:
                continue

            code_match = colonnes[0].get_text(strip=True)
            date_match = colonnes[1].get_text(strip=True)

            # Filtre technique (classement et lignes vides)
            if len(code_match) < 4 or date_match == "" or "Journée" in date_match:
                continue

            # Filtre date
            try:
                date_match_objet = datetime.strptime(date_match, "%d/%m/%y").date()
                if date_match_objet < aujourdhui:
                    continue
            except ValueError:
                continue

            # Filtre équipe spécifique
            equipe_dom = colonnes[3].get_text(strip=True)
            equipe_ext = colonnes[5].get_text(strip=True)
            
            #filtre Mulsanne
            if "MULSANNE" not in equipe_dom.upper() and "MULSANNE" not in equipe_ext.upper() and "ENT.MULSANNE ST-BIEZ ST-OUEN" not in equipe_dom.upper() and "ENT.MULSANNE ST-BIEZ ST-OUEN" not in equipe_ext.upper():
                continue

            # Ajout au tableau final
            match = {
                "Categorie": categorie,
                "Date": date_match,
                "Heure": colonnes[2].get_text(strip=True),
                "Equipe_domicile": equipe_dom,
                "Equipe_exterieur": equipe_ext
            }       
            matchs.append(match)
            
    except Exception as e:
        print(f"Erreur lors de la récupération de {url} : {e}")

matchs.sort(key=lambda x: datetime.strptime(x['Date'], "%d/%m/%y"))
# Sauvegarde unique de la liste fusionnée
with open("matchs.json", "w", encoding="utf-8") as f:
    json.dump(matchs, f, indent=4, ensure_ascii=False)

print(f"Données sauvegardées ({len(matchs)} matchs trouvés au total) !")