# Preps location files: name (lowercase), lat, long

# ===
# PREP CITIES, COUNTRIES
# ===

df_cities = pd.read_csv("worldcitiespop.txt")
df_cities = df_cities[df_cities.Population.notnull()]
df_cities = df_cities.sort(['Population'])
df_cities_large = df_cities[44980:]
df_cities_large_select = df_cities_large[['City','Latitude','Longitude']]
df_cities_large_select.to_csv('cities_large.csv')
#
df_countries = pd.read_csv('countries.csv')
df_countries = df_countries.apply(lambda x: x.astype(str).str.lower())
df_countries = df_countries[['name', 'latitude', 'longitude']]
df_countries.to_csv('countries.csv')
