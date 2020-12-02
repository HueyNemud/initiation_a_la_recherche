import requests
import json
from geocoders.objects.result import result_object
from geocoders.objects import options

# Feature types
address = 'address'
poi = 'poi'
parcel = 'parcel'
location = 'location'
valid_feature_types = [address, poi, parcel, location]

# Options
defaults = {
    'maxResult': 1,
    'precision': 'true',
    'date': 2020
}

# https://geoservices.ign.fr/documentation/services_betas/geocodage.html
# https://geoservices.ign.fr/documentation/services_betas/doc-geocodage.html
def geocode(*queries, opts={}):
    """
    Gécoode un ensemble d'adresses avec le service du géocodeur historique GeoHistoricalData

    :param un nombre variable d'adresses à géocoder
    :param opts: un dictionnaire d'options, cf. https://geoservices.ign.fr/documentation/services_betas/doc-geocodage.html
    :param feature_type: le type d'objet à géocoder, parmis {'address', 'poi', 'parcel', 'location'}
    :return: Un générateur permettant d'itérer sur les résultats de géocodage.
    """

    # Option pre-processing
    options.validate_opts(defaults.keys(), opts)
    opts = options.replace_defaults(defaults, opts)
    opts = options.remove_none_values(opts)

    url = f"http://api.geohistoricaldata.org/geocoding"

    # Calling the geocoder
    for query in queries:
        payload = {**opts, 'address': query}
        res = requests.get(url, params=payload)
        yield _result(query, res)


def _result(query, response):
    if response.status_code != 200:  # Returns a result object even if the geocoding failed.
        return result_object(query, None, response, response.text)
    body = json.loads(response.text)  # The response contains a JSON object.
    return result_object(query, body, response, None)
