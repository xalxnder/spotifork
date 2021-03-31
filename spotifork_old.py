#Scrape album info from Pitchfork 
import requests
import json
album_info = {}
preferred_genres = ['Experimental', 'Rap', 'Electronic']
for page in range(1,4):
    url = f'https://pitchfork.com/reviews/albums/?page={page}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    final = soup.find_all('div', class_= 'review')
    for items in final:
        artist = (items.find('li').string).lower()
        title = (items.find('h2').string).lower()
        genre = (items.find(class_='genre-list__link').string) 
        if genre in preferred_genres:
            album_info.update(
                {artist: title}
            )


with open ('album_info.json', 'w') as file:
    json.dump(album_info, file, indent=4)
