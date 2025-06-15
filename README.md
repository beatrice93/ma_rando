# Ma rando

## Projet

Ce projet a pour but de faciliter la recherche de randonnées accessibles en transports en commun franciliens, à partir de la base de données du site visorando.

Il est constitué d'un notebook de préparation des données, qui extrait les randonnées proches des gares d'IdF depuis visorando avec les informations de dénivelé, longueur, etc., et d'une appli dash qui permet d'explorer le tableau avec différents filtres et options de recherche.

**Note.** Je ne prétends pas remplacer visorando avec cette application, j'ai simplement récupéré les données qui m'intéressaient personnellement et les ai réorganisées selon mes besoins. Si le projet vous intéresse, faites un compte visorando.

## Utilisation

Le projet utilise python 3.12.

### Lancer l'application

Installer les dépendances:
```
pip install -r requirements-app.txt
```

Lancer l'application depuis le terminal:
```
cd dash-app
python src/app.py
```

L'application est disponible à l'adresse `http://127.0.0.1:8050` dans votre navigateur.

### Option : calculer les temps de trajet

Les données nécessaires au fonctionnement de l'application ont déjà été enregistrées. Si vous souhaitez les reproduire, le notebook `scrape_visorando.ipynb` permet de le faire, à condition d'installer les dépendances : 
```
pip install -r requirements-dataprep.txt
```

Il y a également une option pour enrichir le tableau avec le temps de trajet entre votre point de départ et la gare de départ de la randonnée. Pour cela, il faut créer un fichier `.env` à la racine du projet avec les informations suivantes

```env
    PRIM_API_KEY=votre_cle_PRIM
    MY_LOCATION=vos_coordonnees
```

La clé API PRIM permet de calculer un temps de trajet en utilisant l'API PRIM d'IdF mobilités. Cette clé peut être créée en se faisant un compte sur [le site de PRIM](https://prim.iledefrance-mobilites.fr/).

La localisation correspond aux coordonnées de votre point de départ, au format "longitude;latitude", par exemple "2.858667;30.8978964".

