import requests
import json
import os
import sys

def get_playlist_info(playlist):
    baseUrl = 'http://music.163.com/api/playlist/detail?id='
    r = requests.get(baseUrl + playlist, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'})
    contents = r.text
    return contents

def get_songid_arr_from_playlist(playlist_contents):
    playlist_contents_arr = json.loads(playlist_contents)
    tracks_arr = playlist_contents_arr['result']['tracks']
    songs_arr = []
    for track in tracks_arr:
        artists = track['artists']
        artists_arr = []
        for artist in artists:
            artists_arr.append(artist['name'])
        glue = '&'
        artists_str = glue.join(artists_arr)
        each_song = {
            'name' : track['name'],
            'id' : track['id'],
            'artists' : artists_str
            }
        songs_arr.append(each_song)
    return songs_arr

def download_song(song, save_path):
    name = song['name']
    name = name.replace('/', '')
    songid = str(song['id'])
    artists = song['artists']    
    file_name = "%s\\%s-%s.mp3" % (save_path, name, artists)
    if os.path.isfile(file_name):
        print('file existed.\n')
        return 0
    song_outer_link = 'http://music.163.com/song/media/outer/url?id=' + songid
    headers = requests.head(song_outer_link).headers
    if 'Content-Length' in headers:
        print('found songlink: %s\n' % headers['Location'])
    else:
        print('songlink not found\n')
        return 0   
    song_mp3 = requests.get(song_outer_link).content   
    with open(file_name, 'wb') as song_file:
        song_file.write(song_mp3)

if __name__ == '__main__':
    playlist = sys.argv[1]
    save_path = sys.argv[2]
    print("fetching msg from playlist: %s \n" % playlist)    
    playlist_contents = get_playlist_info(playlist)
    if playlist_contents == None:
        print("get songlist contents failed\n")
        exit()
    if not os.path.exists(save_path):
        os.makedirs(save_path) 
    songs_arr = get_songid_arr_from_playlist(playlist_contents)
    for song in songs_arr:
        print("downloading... songid: %s, name: %s, artists: %s\n" % (song['id'], song['name'], song['artists']))
        download_song(song, save_path)


    
