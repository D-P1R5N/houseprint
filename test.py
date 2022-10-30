from urllib import request
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import pprint
"""
This is an example for searching allrecipes and scraping data.

"""

testURL = "https://www.allrecipes.com"
paramURL = "/search/results/?search="
item = "mashed potato"
item = item.replace(' ', '+')
method = 'SEARCH'
#method = 'RECIPE'
x = lambda _ : request.urlopen(_)
url = x(testURL + paramURL + item)
soup = BeautifulSoup(url.read().decode('utf-8'), 'html.parser')
data = json.loads(soup.find('script', type='application/ld+json').text)
if method == 'RECIPE':
    ingredients = data[1]['recipeIngredient']
    #print(data[1]['recipeIngredient'])
elif method == 'SEARCH':
    data = soup.find_all('a', title=True, class_='card__titleLink')
    ratings = soup.find_all('span', class_='review-star-text')
    #Faster, less readable
    _ = [i.text.replace('Rating: ', '').replace(' stars', '') for i in ratings]
    #for r in ratings:
    #    r = r.text.replace('Rating: ', '').replace(' stars', '')
        #print(float(r))
        #print(list(ratings))
    links = list(set(map(lambda x: x.get('href'), data)))
    for r, l in zip(_, links):
        print(r, l, sep='\t')
else:
    print("Neither a search or a recipe.")
url = x(links[1])
soup = BeautifulSoup(url.read().decode('utf-8'), 'html.parser')
data = json.loads(soup.find('script', type='application/ld+json').text)
ingredients = data[1]['recipeIngredient']
print(ingredients)
instructions = data[1]['recipeInstructions']
for ins in instructions:
    print(ins.get('text', "ERROR"))
