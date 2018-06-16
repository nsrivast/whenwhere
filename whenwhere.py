# Finds years and locations in texts, saves down results

import re
import csv
import pdb
import glob
import pickle

import cartopy
import cartopy.crs as ccrs
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
crs = ccrs.PlateCarree()

YEAR_MAX_PLOT = 2100
YEAR_MIN_PLOT = 1200


def get_when(words):
    """ 
    Returns tuples of (nth_word, year) for all 4-digit years found in text
    """
    regex = r"\d{4}"
    when_data = []
    for nth_word, word in enumerate(words):
        match = re.search(regex, word)
        if match:
            year = int(match.group(0))
            when_data.append((nth_word, year))
    
    return when_data


def get_where(words, locations_file):
    """
    Returns tuples of (location, lat, long, count) for all occurrences of location in text
    """
    words = [word.lower() for word in words]
    words_doubles = [words[i] + " " + words[i+1] for i in range(len(words)-1)]
    words_all = words + words_doubles

    with open(locations_file, 'r', encoding='latin-1') as f:
        reader = csv.reader(f)
        locations_data = list(reader)
    
    locations = [loc[1] for loc in locations_data[1:]]
    lats = {loc[1]: loc[2] for loc in locations_data[1:]}
    lngs = {loc[1]: loc[3] for loc in locations_data[1:]}

    where_data = map(lambda x: (x, words_all.count(x)), locations)
    where_data = [r for r in where_data if r[1] > 0]
    where_data.sort(key=lambda r: -r[1])
    
    where_data = [(w[0], lats[w[0]], lngs[w[0]], w[1]) for w in where_data]
    return where_data


def plot_whenwhere(results, fname=False):
    """
    plots whenwhere results, inline or saves to file if fname provided
    """
    when = [r for r in results['when'] if r[1] < YEAR_MAX_PLOT and r[1] > YEAR_MIN_PLOT]
    i_words = [r[0] for r in when]
    if i_words:
        i_words_max = i_words[-1] + 0.0
        i_words_norm = [i/i_words_max for i in i_words]
        year = [r[1] for r in when]
    
        plt.subplot(2, 1, 1)
        plt.scatter(i_words_norm, year)
        plt.title(results['title'])

    lats = [w[1] for w in results['where']]
    lngs = [w[2] for w in results['where']]
    sizes = [w[3]*50 for w in results['where']]
    
    ax = plt.subplot(2, 1, 2, projection=crs)
    ax.set_global()
    ax.coastlines()
    if lats:
        ax.scatter(lngs, lats, s=sizes, transform=crs) # s=sizes, 
    
    if fname:
        plt.savefig(fname)
    else:
        plt.show()
    plt.close()


if __name__ == '__main__':
    """
    LOAD ALL TEXTS, SAVE DOWN PLOTS
    """

    n_start = 0
    txt_files = glob.glob("data/txts/*.txt")
    loc_file = 'data/locations/countries.csv'

    for i, txt_file in enumerate(txt_files[n_start:]):
        title = txt_file.split("/")[-1][:-4]
        print("{}: {}".format(i + n_start, title))

        # open file
        with open(txt_file, "r") as f:
            txt = f.read()
        words = txt.split()

        # find years, locations
        results = { 'title': title }
        results['when'] = get_when(words)
        results['where'] = get_where(words, loc_file)

        # save results
        with open("data/pickled_results/{}.pickle".format(title), "wb") as f:
            pickle.dump(results, f)

        # save plots
        plot_whenwhere(results, "data/plots/{}.png".format(title))



