import re
import csv
import pdb
import matplotlib.pyplot as plt


# ===
# PREP CITIES, COUNTRIES
# ===
# df_cities = pd.read_csv("worldcitiespop.txt")
# df_cities = df_cities[df_cities.Population.notnull()]
# df_cities = df_cities.sort(['Population'])
# df_cities_large = df_cities[44980:]
# df_cities_large_select = df_cities_large[['City','Latitude','Longitude']]
# df_cities_large_select.to_csv('cities_large.csv')
#
# df_countries = pd.read_csv('countries.csv')
# df_countries = df_countries.apply(lambda x: x.astype(str).str.lower())
# df_countries = df_countries[['name', 'latitude', 'longitude']]
# df_countries.to_csv('countries.csv')

# ===
# LOAD, PARSE
# ===
with open("textB.txt", "r") as f:
  s = f.read()
  
s = s.replace("\n", " ")
words = s.split()


# ===
# FIND YEARS
# ===
regex = r"\d{4}"
results = []
for i_word, word in enumerate(words):
  match = re.search(regex, word)
  if match:
    year = int(match.group(0))
    results.append((i_word, year))
    
    
# ===
# PLOT
# ===
if False:
  year_max = 2100
  year_min = 1200
  results_filtered = [r for r in results if r[1] < year_max and r[1] > year_min]

  x = [r[0] for r in results_filtered]
  x_max = x[-1] + 0.0
  x_norm = [i/x_max for i in x]
  y = [r[1] for r in results_filtered]

  plt.scatter(x_norm, y)
  plt.show()


# ===
# LOCATION MATCHES
# ===
words_lower = [wd.lower() for wd in words]
words_doubles = [words_lower[i] + " " + words_lower[i+1] for i in range(len(words_lower)-1)]
#words_triples = [words_lower[i] + " " + words_lower[i+1] + " " + words_lower[i+2] for i in range(len(words_lower)-2)]
words_all = words_lower + words_doubles #+ words_triples

with open('countries.csv', 'rb') as f:
  reader = csv.reader(f)
  country_data = list(reader)
  
countries = [cd[1] for cd in country_data[1:]]

intersects = map(lambda x: (x, words_all.count(x)), countries)
intersects = [r for r in intersects if r[1] > 0]
intersects.sort(key=lambda r: -r[1])
print(intersects)

