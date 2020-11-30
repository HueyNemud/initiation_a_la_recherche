# Installation (Python 3.7+)
Pip est nécessaire, vérifiez qu'il est installé et accessible dans votre console :
```shell script
pip -v
```

Placez vous dans le dossier `initiation_a_la_recherche` puis installez les dépendances requises :
```shell script
pip install -r requirements.txt
```

# Préparation des données

Le code n'est pour le moment prévu que pour les données `dataset_1.csv` des annuaires du commerce (à récupérer sur le GDrive et placer dans le dossier `resources`).
Elles sont chargées à l'aide de l'importeur `datasets/annuaire_du_commerce.py`.

Si vous souhaitez exécuter le code sur un autre jeu de données, il faudra : 
- ajouter le fichier csv dans le dossier `resources`
- ajouter un script d'import dans le dossier `datasets`. Vous pouvez copier et modifier `datasets/annuaires_du_commerce.py`
- éditer le fichier `main.py` pour qu'il exécute votre importeur.

Attention, le code de `main.py` s'attend à trouver une colonne 'address' dans vos données qui contient les chaînes à géocoder.

Cette colonne peut être créée dans l'importeur, comme c'est d'ailleurs le cas pour `annuaire_du_commerce.py` (voir le code). 

 

# Exécution
```shell script
python main.py
```
Le code fonctionne pour le moment avec :
- le *nouveau* géocodeur IGN accessible par API REST : https://geoservices.ign.fr/documentation/services_betas/geocodage.html
- le géocodeur de la Base Adresse Nationale : https://geo.api.gouv.fr/adresse

Les résultats seront stockés dans deux fichiers CSV `annuaire_du_commerce_ban.csv` et `annuaire_du_commerce_ign.csv`.

Le géocodage n'est **jamais** exécuté en batch, chaque adresse est géocodée individuellement. 
Ce code n'est donc pas adapté à du géocodage de données en masse mais seulement à l'évaluation de vos critères. 

# Personnaliser et étendre le code
Le projet est structuré de manière à séparer les différentes tâches dans des modules distincts selon le 
[principe de la responsabilité unique](https://en.wikipedia.org/wiki/Single-responsibility_principle).

Ce code s'appuie largement sur la bibliothèque de traitement de données [Pandas](https://pandas.pydata.org/),
notamment pour charger et sauvegarder les données.

La plupart des personnalisations ne nécessiteront que de modifier `main.py`
  
### `main.py`
`main.py` est le point d'entrée principal du programme. 
La méthode `main()` charge les données à géocoder et 
appelle les méthodes `exec_ban()` et `exec_ign()` qui se chargent d'orchestrer le géocodage des données en utilisant
 un service particulier, de récupérer les résultats et de les enregistrer.

Le chargement des données est réalisé par `datasets/annuaire_du_commerce/dataset_1()`, qui crée aussi une colonne **address** qui joint
les difféntes cellules d'une ligne pour former l'adresse complète à géocoder. 

Ces deux méthodes appellent `run(dataset, geocoder, **kwargs):` qui se charge effectivement d'appeler le géocodeur qu'on lui passe en paramètre
sur toutes les données contenues dans la DataFrame Pandas `dataset`.
 
`run()` prend accepte un ensemble indéfini de paramètres 'mots clés', c'est à dire passés sous la forme `clé=valeur`. 
Ces paramètres sont directement passés au géocodeur, ce qui permet de transmettre les options du géocodeur à la méthode `run()` qui les transmettra.

Par exemple :
```pythonstub

geocoder = ... # Un géocodeur quelconque
dataset = ... # Des données

# Appel de la méthode run avec une paire clé/valeur opts={'toto': 1}
# À l'exécution, run() appellera le géocodeur avec le paramètre supplémentaire : 
# geocoder(item, opts={'toto': 1]) 
run(dataset, geocoder, opts={'toto': 1})
```

### Modifier les options d'un géocoder
Il suffit pour cela d'éditer le dictionnaire `ign_opts` ou `ban_opts` pour ajouter les options souhaitées.

Pour l'IGN, vous pouvez aussi modifier le paramètre `feature_type` qui fixe la catégorie d'objets géographiques à rechercher parmis { address, poi, parcel, location }.

**Important** : toutes les options du géocodeur IGN ne sont pas implémentées, cf. le fichier `geocoders/ign.py`

### Ajouter des mesures, post-traitements, etc.
Le moyen le plus simple est d'ajouter du code dans les méthodes `exec_*()`.

La méthode `run()` renvoie deux objets : (1) la liste des résultats de géocodage et (2) les temps d'exécution de chaque requête.

Les résultats de géocodage sont des dictionnaires Python de la forme suivante :
```pythonstub
{
        'query': query, # La requête qui a été envoyée au géocoder (String)
        'body': body, # La réponse du géocodeur sous forme de dictionnaire python. (Dict)
        'error': error, # Le message d'erreur du géocodeur, s'il y a eu erreur (String ou None)
        'raw': raw_response, # La réponse HTTP brute du géocodeur (String)
        'success': body is not None # Est-ce que le géocodage a réussi ? (Booléen)
    }
``` 
Il peut être plus aisé de les transformer d'abord en tableau Pandas pour travailler dessus : 
```python
all = ign_to_dataframe.transform(results, keep_only=number_of_results)
```






