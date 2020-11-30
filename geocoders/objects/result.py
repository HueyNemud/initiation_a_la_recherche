def result_object(query, body, raw_response, error):
    """
    Retourne une dictionnaire contenant le résultat du géocodage de la requête `query`.
    :param query: la requête à géocoder
    :param body: la réponse du géocodeur sous forme de dictionnaire.
    :param raw_response: la réponse HTTP brute.
    :param error: si le géocodeur a retourné une erreur, contient une description de cette erreur.
    :return: un dictionnaire Python
    """
    return {
        'query': query,
        'body': body,
        'error': error,
        'raw': raw_response,
        'success': body is not None
    }
