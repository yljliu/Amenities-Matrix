import pandas as pd
from typing import Dict

'''Parse 'Amenities Matrix' Sheet from New Database. Return an array of arrays of the lodge names (lodge names were orignally column B of the Amenities Matrix sheet)
Return the first 12 lodge names for testing '''
def get_lodge_names():
    lodge_dataframe = pd.read_excel("C:/Users/Stanl/Downloads/New Database.xlsx", sheet_name = "Amenities Matrix", usecols = "B")
    lodges = lodge_dataframe.values.tolist()

    '''Remove #REF! values'''
    index = 0
    while index < len(lodges):
        if lodges[index][0] != '#REF!':
            index = index + 1
            continue
        del lodges[index]

    return lodges[:50]

'''#Create a new CSV file with the confirmed amenities with respect to the lodge names'''
def create_amenities_dataframe(dictionary: Dict[str, Dict[str, str]]):

    dictionary_to_dataframe = {}

    for key in dictionary:
        list_of_confirmations = []
        amenity = dictionary[key]
        for amen in amenity:
            result = amenity[amen]
            if result[0] == ' ':
                list_of_confirmations.append(' ')
            else:
                total = result[0] + ' - ' + result[1] + ' from ' + result[2]
                list_of_confirmations.append(total)
        dictionary_to_dataframe[key] = list_of_confirmations

    dataframe = pd.DataFrame(dictionary_to_dataframe)
    dataframe = dataframe.transpose()
    dataframe.index.name = 'Lodge Name'
    dataframe.columns = ['Swimming Pool', 'Waterhole', 'Starbed', 'Plunge Pool', 'Private Terrace', 'Landscape View', 'River View', 'Fenced', 'Not Fenced', "Kid's Club", 'Spa', 'Bar', 'Beachfront', 'Beach Access', 'Camp fire', 'Buffet', 'A La Carte', 'Family Room', '24h Power', 'Inside the park']
    dataframe.to_csv('Amenities.csv', index=True, header=True)

