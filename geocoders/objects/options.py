
def validate_opts(whitelist, opts):
    """
    Valide une list d'options à partir d'une liste blanche d'options.
    Une exception est lancée si un élément de `opts` n'est pas dans `whitelist`

    :param whitelist: une liste d'options autorisées.
    :param opts: une liste d'options candidates à valider
    """
    try:
        [obj_in_whitelist(whitelist, opt) for opt in opts]
    except Exception as e:
        message = str(e) + f' \n Valid options are {list(whitelist)}.'
        raise Exception(message)


def obj_in_whitelist(whitelist, var):
    """
    Lance une exception si `var` n'est pas membre de `whitelist`
    :param whitelist: une liste de valeurs valides pour obj
    :param var: une variable à valider
    """
    if var not in whitelist:
        raise Exception(f'Invalid option {var}. Must be one of {whitelist}')


def replace_defaults(defaults, opts):
    """
    Remplace les valeurs des clés du dictionnaire `defaults` qui se trouvent aussi dans le dictionnaire `opts`.
    Cette méthode ne modifie pas les dictionnaires en entrée. Le dictionnaire retourné ne contiendra que les clés de `default`,
    si `opts` contient d'autres clés celles-ci seront ignorées.

    :param defaults: un dictionnaire de valeurs par défaut
    :param opts: un dictionnaire d'options
    :return: une copie de `defaults` dont les valeurs ont été remplacées par celles de `opts` pour les clés qui corespondent.
    """
    return {key: opts.get(key, defaults[key]) for key in defaults}


def remove_none_values(opts):
    """
    Supprime les entrées de valeurs nulles dans un dictionnaire
    :param opts: un dictionnaire
    :return:une copie de `opts` sans les entrées nulles
    """
    o = opts.copy()
    {key: o[key] for key in o.keys() if o[key] is not  None }
    return o
