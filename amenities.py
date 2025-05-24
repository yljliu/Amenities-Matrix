import pandas as pd

#Parse 'Amenities Matrix' Sheet from New Database. Return an array of arrays of the lodge names
def parse_amenities():
    dataframe = pd.read_excel("New Database.xlsx", sheet_name = "Amenities Matrix", usecols = "B")
    lodges = dataframe.values.tolist()
    print(lodges)
    return lodges[:12]

#Create a new CSV file with the new amenities we found
def create_amenities_dataframe(dictionary):

    dataframe = pd.DataFrame(dictionary)
    dataframe = dataframe.transpose()
    dataframe.index.name = 'Lodge Name'
    dataframe.columns = ['Swimming Pool', 'Waterhole', 'Starbed', 'Plunge Pool', 'Private Terrace', 'Landscape View', 'River View', 'Fenced', 'Not Fenced', "Kid's Club", 'Spa', 'Bar', 'Beachfront', 'Beach Access', 'Camp fire', 'Buffet', 'A La Carte', 'Family Room', '24h Power', 'Inside the park']
    dataframe.to_csv('Amenities.csv', index=True, header=True)


