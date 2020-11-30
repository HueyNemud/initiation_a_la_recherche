from geocoders.util.dict_utils import flatten_dict
import pandas as pd


def transform(results, keep_only=1):
    """
    Transforme un ensemble de résultats de géocodage obtenus avec le géocodeur de l'IGN en une DataFrame Pandas.
    :param results: les résultats de géocodage
    :param keep_only: le nombre (non nul) de résultats à conserver pour chaque requête. Par défaut un seul résultat sera retourné par requête.
    :return: une DataFrame Pandas.
    """
    max_matches = max([len(r['body']['features']) for r in results])
    keep_only = min(max_matches, keep_only)

    all_data = [ as_dict(r['body']['features'][:keep_only]) for r in results]
    return pd.DataFrame(all_data)


def as_dict(list_of_features):
    dic = {}
    for idx, feature in enumerate(list_of_features):
        feature['geometry']['lng'] = feature['geometry']['coordinates'][0]
        feature['geometry']['lat'] = feature['geometry']['coordinates'][1]
        del feature['geometry']['coordinates']
        dic = {**dic, **flatten_dict(feature, suffix='_' + str(idx + 1))}
    return dic
