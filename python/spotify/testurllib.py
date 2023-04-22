import urllib.request as urlr


url = 'https://accounts.spotify.com/authorize?client_id=487f97402754478297254b80211a9cba&response_type=code&redirect_uri=https://Santi.com/yo&scope=user-read-playback-state%20user-modify-playback-state%20playlist-read-private%20user-read-currently-playing%20user-read-playback-position%20user-library-modify%20user-library-read%20playlist-modify-private%20playlist-modify-public%20user-top-read'

link = urlr.urlopen(url=url)
print(link.url)