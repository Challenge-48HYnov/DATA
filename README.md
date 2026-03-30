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
```

👉 Et obtenir :

les données météo
les données pollution
l’indice calculé pour cette date

## 🧠 Logique globale (vision produit)

Nous simulons un système capable de fonctionner en temps réel, mais nous travaillons sur un extrait de données maîtrisé.

👉 Le pipeline doit être :

- clair
- reproductible
- structuré
- exploitable via une API

## ⚙️ Pipeline Data

### 1. Ingestion

#### Sources :

- Données pollution (ATMO – temps réel, moyennes horaires)
- Données météo (SYNOP)

### 2. Nettoyage

#### Pollution
##### garder :

Colonne	            Utilité
Date de début	        Pour indexer les mesures dans le temps
Date de fin	          Pour interpolation horaire si nécessaire
Polluant	            Type de polluant (NO, O3, PM10…)
valeur	              Valeur validée du polluant
unité de mesure	      Pour normaliser toutes les mesures
code site / nom site	Identification des stations (utile pour jointure GPS)
type d'implantation	  Pondération selon zone urbaine / rurale
type d’influence	    Pondération selon trafic / industriel / fond
validité	            Pour filtrer ou pondérer les valeurs

Facultatif si besoin pour debug ou API : Organisme

#### Météo

##### garder :

Colonne	              Utilité
lat / lon	            Coordonnées GPS pour la jointure géospatiale
reference_time	      Pour indexer dans le temps
t	                    Température
dd / ff	              Vent (direction et vitesse)
Humidité (u)	        Impact sur l’indice
Pluie (rr1, rr24)	    Pour ajuster dispersion polluants

### 3. Transformation

uniformiser les dates (format datetime)
filtrer une période (ex : 2–3 jours)
éventuellement limiter à une zone/station

#### Important avant jointure : 

Ordre des opérations : GPS avant fusion

Il faut faire le calcul de distance GPS avant la fusion, pour ces raisons :

Les fichiers ne sont pas matchables directement par station (nom site n’existe pas côté météo).
On a besoin de savoir quelle station météo est la plus proche de chaque station pollution.
Une fois qu’on a trouvé le “plus proche”, on peut fusionner les fichiers en fonction du temps (par heure ou par quart d’heure) pour créer l’indice.

Donc :

Étape 1 : Calculer la station météo la plus proche pour chaque station pollution (Haversine).
Étape 2 : Fusionner pollution + météo selon temps et station météo associée.
Étape 3 : Calculer l’indice pondéré pollution × météo.
Étape 4 : Préparer la table finale pour l’API.



### 4. Jointure (fusion)

fusion sur :

- date
- station (ou station proche)


##### 👉 Objectif :
Créer un dataset unique :

date, station, pm10, pm25, no2, temperature, wind, rain

### 5. Calcul de l’indice

Créer un ou plusieurs indices :

```bash
indice = (pm25 * 0.5 + pm10 * 0.3 + no2 * 0.2) - (vent * 0.2 + pluie * 0.1)
```

👉 L’indice doit être :

- cohérent
- justifié
- documenté

### 6. Output

Dataset final :

date, station, indice

👉 Utilisé par l’API pour répondre aux requêtes utilisateurs

```bash

🗂️ Structure du repo
data/
│
├── raw/               # données brutes téléchargées
├── processed/         # données nettoyées
├── final/             # dataset fusionné + indices
├── scripts/           # scripts Python
└── README.md

```

## 👩‍💻 Répartition des tâches

### 👤 Personne 1 — Pollution

- télécharger dataset ATMO
- nettoyer données
- filtrer polluants (NO2, PM10, PM2.5)
- faire pivot ( Transformer les lignes polluans en colonne ).
- exporter pollution_clean.csv

### 👤 Personne 2 — Météo

- récupérer SYNOP
- sélectionner variables utiles
- nettoyer données
- exporter meteo_clean.csv

### 👤 Personne 3 — Fusion & Indice

- fusionner pollution + météo
- gérer les dates
- calculer l’indice
- exporter final_dataset.csv

## 🔁 Fonctionnement côté API (important)

👉 L’API ne recalcule pas tout

Elle fait :

```bash
df[df["date"] == date]
```

👉 Donc :

les données doivent être prêtes
bien indexées par date

## ⚠️ Contraintes & choix techniques

### ✔ CSV plutôt qu’API

- plus stable
- plus rapide à implémenter
- moins de risques en 48h

👉 Possibilité d’ajouter API plus tard (bonus)

### ✔ Données limitées
1 zone ou 1 station recommandée
quelques jours seulement

👉 Objectif : qualité > quantité

### ✔ Pipeline simple et propre

- pas de complexité inutile
- priorité à la cohérence

## 🚀 Bonus (optionnel)

- régression linéaire simple pour prédiction
- simulation temps réel
- ajout de coordonnées GPS



✅ Résultat attendu

- dataset propre
- indice cohérent
- API simple et fonctionnelle
- code structuré et lisible


➡️ ingestion

➡️ transformation

➡️ modélisation

➡️ exposition via API
