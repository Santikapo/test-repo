from requests import get, post, put
from userinfo import client_id, client_secret
import base64
import time
import os
clear = lambda: os.system('cls')
import urllib.request

auth_string = client_id + ":" + client_secret
auth_bytes = auth_string.encode("utf-8")
auth = str(base64.b64encode(auth_bytes), "utf-8")


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
            

    request = get(url + f'client_id={client_id}&response_type=code&redirect_uri=https://Santi.com/yo&scope={scopes}')
    
    print (url + f'client_id={client_id}&response_type=code&redirect_uri=https://Santi.com/yo&scope={scopes}')

def get_access_token(test):
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization" : "Basic " + auth,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type" : "authorization_code",
        "code" : test,
        "redirect_uri" : 'https://Santi.com/yo', 
    }



    answer = post(url=url, headers=headers, data=data).json()
    print(answer)
    
    # saving refresh token
    f = open("tokens.txt", "w")
    f.write(answer['access_token'] + '\n')
    f.write(answer['refresh_token'] + '\n')
    f.close()
    return answer['access_token']

def use_refresh():
    f = open("tokens.txt", "r")
    f.readline()
    refresh = f.readline().rstrip('\n')
    f.close()
    
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization" : 'Basic ' + auth,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type" : 'refresh_token',
        "refresh_token" : refresh,
    }



    answer = post(url=url, headers=headers, data=data).json()

    f = open("tokens.txt", "w")
    f.write(answer['access_token'] + '\n')
    f.write(refresh + '\n')
    f.close()

    newtoken = answer['access_token']
    return newtoken

def get_new_code(token):
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization" : "Basic " + auth,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type" : "refresh_token",
        "refresh_token" : token,
    }

    return post(url=url, headers=headers, data=data).json()

def get_playlists(token):

    headers = {
            "Authorization" : "Bearer " + token, 
            "Content-Type" : "application/json",
            #"Accept" : "application/json"
        }
        

    yo = get(url='https://api.spotify.com/v1/me/playlists', headers=headers).json()

    for i in yo['items']:
        print(i['name'])

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
    total = 0
    while True:
        batch = get(url=f'https://api.spotify.com/v1/me/tracks?limit=50&offset={offset}', headers=headers).json()
        total = int(batch['total'])
        for items in batch['items']:
            liked.append(items['track']['id'])
        clear()
        percent = offset/total*100

        print('%.0f' % percent, end='%\n')
        
        if len(batch['items']) < 50:
            clear()
            print('100%')
            break
        offset += 50

    print(f'Loaded {total} tracks')

def skip_liked(token, checking):
    headers = {
            "Authorization" : "Bearer " + token, 
            "Content-Type" : "application/json",
            #"Accept" : "application/json"
        }
        

    song = get(url='https://api.spotify.com/v1/me/player/currently-playing', headers=headers).json()['item']

    if song['id'] in liked:
        print('skipped ' + song['name'])
        skip(token, checking)

def skip(token, checking):
    headers = {
            "Authorization" : "Bearer " + token, 
            "Content-Type" : "application/json",
            #"Accept" : "application/json"
        }
        

    post(url='https://api.spotify.com/v1/me/player/next', headers=headers)
    time.sleep(0.1)
    if checking == True:
        skip_liked(token, checking)
