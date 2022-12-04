
import requests
import json
import pandas as pd
import base64
from bs4 import BeautifulSoup

PREFERRED_GENRES = ['Experimental', 'Rap', 'Electronic']


def get_album_info():
	album_info = []
	for page in range(1, 4):
		url = f'https://pitchfork.com/reviews/albums/?page={page}'
		req = requests.get(url)
		soup = BeautifulSoup(req.content, 'html.parser')
		reviews = soup.find_all('div', class_='review')
		for items in reviews:
			try:
				artist = (items.find('li').string).lower()
				title = (items.find('h2').string).lower()
				genre = (items.find(class_='genre-list__link'))
				if genre != None and genre.text in PREFERRED_GENRES:
					album_info.append(
						{'artist': artist,
						 'title': title
						 }
					)
			except:
				pass
	return album_info
