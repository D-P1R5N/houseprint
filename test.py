from urllib import request
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import pprint
"""
This is an example for searching allrecipes and scraping data.

"""
testURL = "https://www.allrecipes.com/recipe/232061/baja-style-fish-tacos/"
x = request.urlopen(testURL)
soup = BeautifulSoup(x.read().decode('utf-8'), 'html.parser')
data = json.loads(soup.find('script', type='application/ld+json').text)
if 'recipeIngredient' in data[1]:
    ingredients = data[1]['recipeIngredient']
    print(data[1]['recipeIngredient'])
