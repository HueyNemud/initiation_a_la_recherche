from geocoders.util.dict_utils import flatten_dict
import pandas as pd


def transform(results, keep_only=1):
    """
    Transforme un ensemble de résultats de géocodage obtenus avec le géocodeur GHD en une DataFrame Pandas.
    :param results: les résultats de géocodage
    :param keep_only: le nombre (non nul) de résultats à conserver pour chaque requête. Par défaut un seul résultat sera retourné par requête.
    :return: une DataFrame Pandas.
    """
    if keep_only < 1 or not isinstance(keep_only,int):
        raise Exception(f"keep_only must be a positive integer, not {keep_only}")

    max_matches = max([len(r) for r in results])
    keep_only = min(max_matches, keep_only)
    all_data = [as_dict(r['body'][:keep_only]) for r in results]
    return pd.DataFrame(all_data)


def as_dict(list_of_features):
    dic = {}
    for idx, feature in enumerate(list_of_features):
        if feature['geography']['type'] == 'GeometryCollection':
            feature['geography']['lng'] = feature['geography']['geometries'][0]['coordinates'][0][0]
            feature['geography']['lat'] = feature['geography']['geometries'][0]['coordinates'][0][1]
            del feature['geography']['geometries']
        else:
            feature['geography']['lng'] = feature['geography']['coordinates'][0][0]
            feature['geography']['lat'] = feature['geography']['coordinates'][0][1]
            del feature['geography']['coordinates']

        del feature['geography']['type']

        dic = {**dic, **flatten_dict(feature, suffix='_' + str(idx + 1))}
    return dic
