from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date = input("Which Year You Want To Travel To ? Type The Date I This Format YYYY-MM-DD:")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="Playlist-modify-private",
        redirect_uri="http://developer.spotify.com/?code=ACKJ26V4YJJAemSlmrCK1KVApowlbbck9_jrNHGzmlgevE0me_dK",
        client_id = "6004v306d8e29f49599444893076gh",
        client_secret = "845uh295n0m4sd8994gh436045zp30y",
        show_dialog = True,
        cache_path = "token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify.Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

