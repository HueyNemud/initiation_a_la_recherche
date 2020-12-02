import geocoders.ban as ban
import geocoders.ign as ign
import geocoders.ghd as ghd
from statistics import median, stdev, mean
from timeit import default_timer as timer
from datasets import annuaires_du_commerce
from geocoders.util import ban_to_dataframe, ign_to_dataframe, ghd_to_dataframe
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(message)s')


# Méthode principale
def main():
    ds1 = annuaires_du_commerce.dataset_1()  # Charge les données à géocoder
    exec_ghd(ds1)  # Géocode avec le service IGN et sauvegarde le résultat
    #exec_ign(ds1)  # Géocode avec le service IGN et sauvegarde le résultat
    #exec_ban(ds1)  # Géocode avec le service BAN et sauvegarde le résultat


def exec_ban(dataset):
    # Définit les options de géocodage
    number_of_results = 1
    ban_opts = {'limit': number_of_results, 'citycode': 75056}  # Force à chercher dans Paris

    # Géocode le contenu de la colonne 'address' dans dataset.
    logging.info(f'Executing BAN geocoder with options {ban_opts}')
    geocoder = ban.geocode
    results, runtimes = run(dataset['address'], geocoder, opts=ban_opts)

    # Affiche les statistiques de temps d'exécution
    summary(dataset, results, runtimes)

    # Transforme les résultats renvoyés par le géocodeur en tableau Pandas
    all = ban_to_dataframe.transform(results, keep_only=number_of_results)

    # Concatène le tableau des résultats aux données d'entrée et sauvegarde le résultat
    pd.concat([dataset, all], axis=1).to_csv('annuaire_du_commerce_ban.csv')


def exec_ign(dataset):
    # Définit les options de géocodage
    number_of_results = 1
    ign_opts = {'maxResp': number_of_results}

    # Géocode le contenu de la colonne 'address' dans dataset.
    logging.info(f'Executing IGN geocoder')
    addresses_plus_paris = dataset['address'] + ' 75'  # Force à chercher dans Paris (75)
    results, runtimes = run(addresses_plus_paris, ign.geocode, feature_type='address', opts= ign_opts)

    # Affiche les statistiques de temps d'exécution
    summary(dataset, results, runtimes)

    # Transforme les résultats renvoyés par le géocodeur en tableau Pandas
    all = ign_to_dataframe.transform(results, keep_only=number_of_results)

    # Concatène le tableau des résultats aux données d'entrée et sauvegarde le résultat
    pd.concat([dataset, all], axis=1).to_csv('annuaire_du_commerce_ign.csv')

def exec_ghd(dataset):
    # Définit les options de géocodage
    number_of_results = 1
    ghd_opts = {'date': 1820}

    # Géocode le contenu de la colonne 'address' dans dataset.
    logging.info(f"Executing GHD geocoder (date = {ghd_opts.get('date')})")
    addresses_plus_paris = dataset['address'] + ' Paris'  # Force à chercher dans Paris (75)
    results, runtimes = run(addresses_plus_paris, ghd.geocode, opts= ghd_opts)

    # Affiche les statistiques de temps d'exécution
    summary(dataset, results, runtimes)

    # Transforme les résultats renvoyés par le géocodeur en tableau Pandas
    all = ghd_to_dataframe.transform(results, keep_only=number_of_results)

    # Concatène le tableau des résultats aux données d'entrée et sauvegarde le résultat
    pd.concat([dataset, all], axis=1).to_csv('annuaire_du_commerce_ghd.csv')




def run(dataset, geocoder, **kwargs):
    """
    Geocode a dataset using a geocoder.
    :param dataset: a dataset to geocode
    :param geocoder: the geocoder to use
    :return:
    """
    results, runtimes = [], []

    data_list = list(dataset)
    data_len = len(data_list)
    for idx, item in enumerate(data_list):
        # Appelle le géocodeur passé en paramètres avec l'item à géocoder et les options passées à la méthode et
        # mesure le temps d'exécution
        start = timer()
        r = next(geocoder(item, **kwargs))
        elapsed_time = timer() - start

        results.append(r)
        runtimes.append(elapsed_time)

        # Affiche le géocodage courant
        log = '\u2713' if r['success'] else '\u2728'
        log += f" {idx + 1}/{data_len} {elapsed_time * 1000}ms: \'{item}\'"
        log += '' if r['success'] else r['error']
        logging.info(log)

    return results, runtimes


def summary(dataset, results, times):
    """
    Print some information about the execution time of a geocoding
    """
    succ, fail = [], []

    [succ.append(r) if r['success'] else fail.append(r) for r in results]

    logging.info(
        f'Geocoding {len(dataset)} addresses took {sum(times)}s'
        f' with {len(succ)} successes and {len(fail)} failures'
        f' (min = {min(times)}s,'
        f' max = {max(times)}s,'
        f' avg = {mean(times)}s,'
        f' stddev = {stdev(times)}s,'
        f' median = {median(times)}s)')


if __name__ == '__main__':
    main()
