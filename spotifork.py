import http
import requests
import json
import base64
from bs4 import BeautifulSoup
from secrets import *

SEARCH_URL ='https://api.spotify.com/v1/search'
PREFERRED_GENRES = ['Experimental', 'Rap', 'Electronic']

album_search_ids = []
track_ids = []
album_info = {}
current_playlist_ids = []

#Scrape the Pitchfork review pages
for page in range(1,4):
    url = f'https://pitchfork.com/reviews/albums/?page={page}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    final = soup.find_all('div', class_= 'review')
    for items in final:
        artist = (items.find('li').string).lower()
        title = (items.find('h2').string).lower()
        genre = (items.find(class_='genre-list__link'))
        if genre != None and genre.text in PREFERRED_GENRES:
            album_info.update(
                {artist: title}
            )
# #Save the results to json file.
with open ('album_info.json', 'w') as file:
    json.dump(album_info, file, indent=4)

#Get albums from json file and then search.
with open('album_info.json') as file:
    data = json.load(file)
    for artist, album in data.items():
      print(f'Searching for......{artist} - {album}')
      header ={'Authorization':'Bearer' + ' ' +  get_refresh_token()}
      payload  = {'q':album,
      'type':'album'
      }
      r = requests.get(SEARCH_URL,params=payload, headers=header).json()
      results = r['albums']['items']
      for i in results:
            album_id = i['id']
            artists_dict = i['artists']
            if i['album_type'] == 'album' and i['name'].lower() == album:
                  for info in artists_dict:
                        artists = info['name'].lower()
                        if artists in data:
                              uri = album_id
                              album_search_ids.append(uri)


#Get current playlist song ids to check for duplicates
for i in range(0,400,100):
    playlsit_tracks_request = requests.get('https://api.spotify.com/v1/playlists/0SKeG4r7Ui7jGORNGAdYNS/tracks?offset='+ str(i), headers=header).json()
    playlsit_tracks_results = playlsit_tracks_request['items']
    for i in playlsit_tracks_results:
        current_playlist_ids.append(i['track']['uri'])
      

#Get Songs from albums, by ID, and add them to my playlist.
for ids in album_search_ids:
      tracks_request = requests.get('https://api.spotify.com/v1/albums/'+ids+'/tracks', headers=header).json()
      for i in tracks_request['items']:
            track_uri = i['uri']
            #Check for duplicates
            if track_uri not in current_playlist_ids:
                add_request = requests.post('https://api.spotify.com/v1/playlists/'+PLAYLIST_ID+'/tracks', params='uris='+track_uri,headers=header)
                print(f'Adding {track_uri}')
                print(i['name'])
            else:
                print('Skipping')
                  
