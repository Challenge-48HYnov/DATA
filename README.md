# 📊 Data Pipeline – Indice Pollution & Météo

## 🎯 Objectif du projet

L’objectif de ce repository est de construire un **pipeline de données** permettant de :

- récupérer des données de **pollution** et de **météo**
- les **nettoyer et les structurer**
- les **fusionner intelligemment**
- calculer un **indice combiné**
- mettre ces données à disposition via un **endpoint pour les développeurs**

👉 L’utilisateur final pourra demander :

```bash
GET /indices?date=2026-03-10


👉 Et obtenir :

les données météo
les données pollution
l’indice calculé pour cette date
🧠 Logique globale (vision produit)

Nous simulons un système capable de fonctionner en temps réel, mais nous travaillons sur un extrait de données maîtrisé.

👉 Le pipeline doit être :

clair
reproductible
structuré
exploitable via une API
⚙️ Pipeline Data
1. Ingestion

Sources :

Données pollution (ATMO – temps réel, moyennes horaires)
Données météo (SYNOP)
2. Nettoyage
Pollution
garder :
date
station
polluant (NO2, PM10, PM2.5)
valeur
transformer en format large (pivot)
Météo
garder :
date
station
température
vent
pluie
3. Transformation
uniformiser les dates (format datetime)
filtrer une période (ex : 2–3 jours)
éventuellement limiter à une zone/station
4. Jointure (fusion)
fusion sur :
date
station (ou station proche)

👉 Objectif :
Créer un dataset unique :

date, station, pm10, pm25, no2, temperature, wind, rain
5. Calcul de l’indice

Créer un ou plusieurs indices :

indice = (pm25 * 0.5 + pm10 * 0.3 + no2 * 0.2) - (vent * 0.2 + pluie * 0.1)

👉 L’indice doit être :

cohérent
justifié
documenté
6. Output

Dataset final :

date, station, indice

👉 Utilisé par l’API pour répondre aux requêtes utilisateurs

🗂️ Structure du repo
data/
│
├── raw/               # données brutes téléchargées
├── processed/         # données nettoyées
├── final/             # dataset fusionné + indices
├── scripts/           # scripts Python
└── README.md
👩‍💻 Répartition des tâches
👤 Personne 1 — Pollution
télécharger dataset ATMO
nettoyer données
filtrer polluants (NO2, PM10, PM2.5)
faire pivot
exporter pollution_clean.csv
👤 Personne 2 — Météo
récupérer SYNOP
sélectionner variables utiles
nettoyer données
exporter meteo_clean.csv
👤 Personne 3 — Fusion & Indice
fusionner pollution + météo
gérer les dates
calculer l’indice
exporter final_dataset.csv
🔁 Fonctionnement côté API (important)

👉 L’API ne recalcule pas tout

Elle fait :

df[df["date"] == date]

👉 Donc :

les données doivent être prêtes
bien indexées par date
⚠️ Contraintes & choix techniques
✔ CSV plutôt qu’API
plus stable
plus rapide à implémenter
moins de risques en 48h

👉 Possibilité d’ajouter API plus tard (bonus)

✔ Données limitées
1 zone ou 1 station recommandée
quelques jours seulement

👉 Objectif : qualité > quantité

✔ Pipeline simple et propre
pas de complexité inutile
priorité à la cohérence
🚀 Bonus (optionnel)
régression linéaire simple pour prédiction
simulation temps réel
ajout de coordonnées GPS
🎤 Argumentaire (pour soutenance)

Nous avons conçu un pipeline permettant de traiter des données environnementales afin de produire un indice combiné pollution/météo.
Le système est structuré pour répondre à des requêtes par date, avec une architecture compatible avec un usage temps réel.

✅ Résultat attendu
dataset propre
indice cohérent
API simple et fonctionnelle
code structuré et lisible
💬 Conclusion

Ce projet n’est pas seulement une analyse de données, mais la construction d’un système data complet :

➡️ ingestion
➡️ transformation
➡️ modélisation
➡️ exposition via API
