#Create spotify playlist based on Pitchfork Reviews 
from bs4 import BeautifulSoup
import requests
import json
url = 'https://pitchfork.com/reviews/albums/'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
review_lst = soup.find_all('div', class_= 'fragment-list')
final = soup.find_all('div', class_= 'review')
album_info = {}
preferred_genres = ['Experimental', 'Rap', 'Electronic']
for items in final:
    artist = (items.find('li').string)
    title = (items.find('h2').string)
    genre = (items.find(class_='genre-list__link').string) 
    if genre in preferred_genres:
        album_info.update(
            {artist: title}
        )


with open ('album_info.json', 'w') as file:
    json.dump(album_info, file, indent=4)
