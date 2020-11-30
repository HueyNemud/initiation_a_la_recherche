import pandas as pd


def dataset_1():
    """
    Return data from 'resources/dataset_1.csv' as a Pandas DataFrame with a column 'address'
    containing the full address (number + type + street).
    :return: a Pandas DataFrame holding the data from 'resources/dataset_1.csv'
    """
    csv = pd.read_csv('resources/dataset_1.csv') # Pandas loads the CSV file as a DataFrame object
    csv.fillna('', inplace=True) # Pandas fills empty celles with NaN. We replace every Nan value with an emtpy string.
    csv.num_rue = csv.num_rue.apply(str)  # Cast street numbers to strings
    # Create a new column named 'address' which concatenates the columns ['num_rue', 'cpltnum_ru', 'type_rue', 'article_ru', 'nom_rue']
    # csv[['num_rue', 'cpltnum_ru', 'type_rue', 'article_ru', 'nom_rue']]  select a subset of the table 'csv'.
    # .agg(' '.join, axis=1) is equivalent to merge the selected cells of every lines as 'num_rue' + ' ' + 'cpltnum_ru' + ' ' + 'type_rue' + ' ' + 'article_ru' + ' ' + 'nom_rue'
    csv['address'] = csv[['num_rue', 'cpltnum_ru', 'type_rue', 'article_ru', 'nom_rue']].agg(' '.join, axis=1)
    return csv
