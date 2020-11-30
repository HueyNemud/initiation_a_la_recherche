import requests
import json
from geocoders.objects import options
from geocoders.objects.result import result_object

defaults = {
    'limit': 1,
    'autocomplete':0,
    'lat': '',
    'long': '',
    'postcode': '',
    'citycode': '',
    'type': ''
}


# https://geo.api.gouv.fr/adresse
def geocode(*queries, opts={}):
    """
    Gécoode un ensemble d'adresses avec le service de la *Base Adresse Nationale*
    :param un nombre variable d'adresses à géocoder
    :param opts: un dictionnaire d'options, cf. https://geo.api.gouv.fr/adresse
    :return: Un générateur permettant d'itérer sur les résultats de géocodage.
    """

    url = f'https://api-adresse.data.gouv.fr/search/'

    # Option pre-processing
    options.validate_opts(defaults.keys(), opts)
    opts = options.replace_defaults(defaults, opts)

    # Calling the geocoder
    for query in queries:
        payload = {**opts, 'q': query}
        res = requests.get(url, params=payload)
        yield _result(query, res)


def _result(query, response):
    if response.status_code != 200:
        return result_object(query, None, response, response.text)

    body = json.loads(response.text)
    return result_object(query, body, response, None)
