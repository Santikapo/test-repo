import os
import base64
from requests import get, post, put
import json
import webbrowser
import sched
import time

client_id = "487f97402754478297254b80211a9cba"
client_secret = 'e97308179f2642cebceadc67e5b58346'
code = 'AQDKdCff_HCKequOw2MRbIE1uXi-CNsr44RcZ318O_wzmw_yfdxSFrBOhq8V-6c1dBf73i9lVkl3gNOOaCzGcxuoJQAviQ6YbdLbsnDgshhiwrwcbA4B6EvSVZurtnrTDYp32SHLTg7bkVxkOruSE_tMoA0TTgU8FNDyllEnPma1GTu-irdYg7McxRPYdvAExVSm-ryMVLNFgkr0d7dKGN4vIs1Eoies-CTZ8JMGxS4eE7w9j-PLvLRV0zlLUasOmj1JaxL0XZzd626EqKzbZWatfP50F2Jeo5xx5Rw1wH-29xc6eapqh99Z5veEHb9VlxgNBsCSk8zbXZ4RUpSxm0_kaQHp1q0vOS8ZGjWuls92ZMqP38F_UqjY04qoviGUt_yi8-gYOMMCuFK_KoDXg97Wo7VTuQRwXpTdlVdsCgAHpFO-3UjyPIuDvqEyN3kzy9C_nooqVxtPgSKH__u6mpe3A4gwQx4'
refresh = 'AQC-2SAkRZwV8TKY_d5resinykAmAEX_aUKXI-9FIC8pPZwSjWPE99Lo9sen69sXYEPFhCUGwsx6Vbw11A-Xc84JQM-drF3bUdbsEcYdgtea2CGeZEmUz65QM8yWphV5DMo'
wb = webbrowser.BaseBrowser 
liked = []
def get_code():

    url = "https://accounts.spotify.com/authorize?"

    # permisions of what I can access
    scopes = 'user-read-playback-state' + '%20' +\
             'user-modify-playback-state' + '%20' +\
             'playlist-read-private' + '%20' +\
             'user-read-currently-playing' + '%20' +\
             'user-read-playback-position' + '%20' +\
             'user-library-modify' + '%20' +\
             'user-library-read' + '%20' +\
             'playlist-modify-private' + '%20' +\
             'playlist-modify-public' + '%20' +\
             'user-top-read'
            

    result = get(url + f'?client_id={client_id}&response_type=code&redirect_uri=https://Santi.com/yo&scope={scopes}')
    print (url + f'client_id={client_id}&response_type=code&redirect_uri=https://Santi.com/yo&scope={scopes}')


def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    #print(auth_base64)
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri" : 'https://Santi.com/yo', 
    }

    answer = post(url=url, headers=headers, data=data).json()
    print(answer)

def get_new_code(token):
    url = 'https://accounts.spotify.com/api/token'
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    #print(auth_base64)
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type" : "refresh_token",
        "refresh_token" : token,
    }


    return post(url=url, headers=headers, data=data).json()[acc]


def get_tracks(token):

    headers = {
            "Authorization" : "Bearer " + token, 
            "Content-Type" : "application/json",
            #"Accept" : "application/json"
        }
        

    yo = get(url='https://api.spotify.com/v1/me/playlists', headers=headers).json()

    for i in yo['items']:
        print(i['name'])

#token = get_token()
token = 'BQDrsT7HuaIf_XDFamomiRbVC9hH9K8eVkkuGnc_mKrVzfb4n3v_kfaay-qfxdmhTwmHjDi91t_5rP3elyc1ho3X_9t-wZ-Uy5WuyrrMeUWFLsaHOqZF4D5DBaaE5MiX7-4pAu4xRpZKbfLaM-dAwM8Jp-yzR39qTKh9DKWgj2tPtw7_B2j4XWG8lVkLkEDYeJI0dqvbpsiioa0ws3U5VP-_t5PW4TKvHGPiOj6Vwkgf8vk_uh6HLZI_RNDUpw-BVwt2hF3OpW8iQzsliBG4sexn9YbE6Jl6XanmRoPpmEJVeSh3uQ'
def start_resume(token):


    headers = {
            "Authorization" : "Bearer " + token, 
            "Content-Type" : "application/json",
            #"Accept" : "application/json"
        }
        

    yo = put(url='https://api.spotify.com/v1/me/player/play', headers=headers)

def get_liked(token):
    offset = 0
    headers = {
        "Authorization" : "Bearer " + token, 
        "Content-Type" : "application/json",
        #"Accept" : "application/json"
    }

    while True:
        batch = get(url=f'https://api.spotify.com/v1/me/tracks?limit=50&offset={offset}', headers=headers).json()

        for items in batch['items']:
            liked.append(items['track']['id'])

        if len(batch['items']) < 50:
            #if True:
            break
        offset += 50

    #print(sorted(liked))

def skip_liked(token):
    print('checking')
    headers = {
            "Authorization" : "Bearer " + token, 
            "Content-Type" : "application/json",
            #"Accept" : "application/json"
        }
        

    song_id = get(url='https://api.spotify.com/v1/me/player/currently-playing', headers=headers).json()['item']['id']
    print(song_id)
    if song_id in liked:
        skip(token)


def skip(token):
    headers = {
            "Authorization" : "Bearer " + token, 
            "Content-Type" : "application/json",
            #"Accept" : "application/json"
        }
        

    post(url='https://api.spotify.com/v1/me/player/next', headers=headers)
    print('skipped')
    skip_liked(token)
  
def periodic(scheduler, interval, action, actionargs):

    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(actionargs)

#get_code()
#get_access_token()
#get_tracks(token)
#start_resume(token)
get_liked(token)
scheduler = sched.scheduler(time.time, time.sleep)
periodic(scheduler, 5, skip_liked, token)