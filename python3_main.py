import requests
import os
import sys

def get_json(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'})
    return r.json()

def mk_artists(parrent):
    artists = parrent['artists']
    artists_arr = []
    for artist in artists:
        artists_arr.append(artist['name'])
    glue = ' ft. '
    return glue.join(artists_arr)

def get_song_info(songid):
    url = 'http://music.163.com/api/song/detail/?id=' + songid + '&ids=[' + songid +']'
    res = get_json(url)
    songs = res['songs'][0]
    return {
        'name' : songs['name'],
        'id' : songs['id'],
        'artists' : mk_artists(songs)
        }

def get_playlist_info(playlist):
    url = 'http://music.163.com/api/playlist/detail?id=' + playlist
    return get_json(url)

def get_songs_arr_from_playlist(playlist_json):
    tracks_arr = playlist_json['result']['tracks']
    songs_arr = []
    for track in tracks_arr:
        each_song = {
            'name' : track['name'],
            'id' : track['id'],
            'artists' : mk_artists(track)
            }
        songs_arr.append(each_song)
    return songs_arr

def download_song(song, target_dir):
    print("\nDownloading... songid: %s, name: %s, artists: %s" % (song['id'], song['name'], song['artists']))
    name = song['name']
    name = name.replace('/', '')
    songid = str(song['id'])
    artists = song['artists']
    file_name = "%s\\%s-%s.mp3" % (target_dir, name, artists)
    if os.path.isfile(file_name):
        print('File already existed.')
        return 0
    song_outer_url = 'http://music.163.com/song/media/outer/url?id=' + songid
    headers = requests.head(song_outer_url).headers
    if 'Content-Length' in headers:
        print('Found songlink: %s' % headers['Location'])
    else:
        print('Songlink not found')
        return 0
    song_mp3 = requests.get(song_outer_url).content   
    with open(file_name, 'wb') as song_file:
        song_file.write(song_mp3)
        print('Mp3 file saved')

def get_mv_info(mv_id):
    url = 'http://music.163.com/api/mv/detail?id=%s' % mv_id
    return get_json(url)

def download_mv(mv_json, target_dir, clarity):
    
    clarities = ['240', '480', '720', '1080']
    if clarity not in clarities:
        clarity = 1080
        print('automate select, clarity = 1080')
    data = mv_json['data']
    name = data['name']
    artists = mk_artists(data)
    print("\nDownloading... mv id: %s, name: %s, artists: %s" % (mv_json['data']['id'], name, artists))
    cover_url = data['cover']
    cover = "%s\\%s-%s.jpg" % (target_dir, name, artists)
    if os.path.isfile(cover):
        print('Cover already existed.')
    else:
        print('downloading...')
        cover_content = requests.get(cover_url).content 
        with open(cover, 'wb') as cover_file:
            cover_file.write(cover_content)
            print('Cover saved')
    
    video_url = data['brs'][clarity]
    video = "%s\\%s-%s.mp4" % (target_dir, name, artists)
    if os.path.isfile(video):
        print('Video already existed.')
    else:
        print('downloading...')
        video_content = requests.get(video_url).content 
        with open(video, 'wb') as video_file:
            video_file.write(video_content)
            print('Video saved')
    
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        exit('Not enough arguments')
    mode = sys.argv[1]
    target_dir = sys.argv[2]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir) 
    if mode == 'song':
        songid = str(sys.argv[3])
        song = get_song_info(songid)
        download_song(song, target_dir)
    elif mode == 'playlist':
        playlist = sys.argv[3]
        print("Get msg from playlist: %s" % playlist)
        playlist_json = get_playlist_info(playlist)
        if playlist_json == None:
            print("Get songlist contents failed")
            exit()
        if not os.path.exists(target_dir):
            os.makedirs(target_dir) 
        songs_arr = get_songs_arr_from_playlist(playlist_json)
        for song in songs_arr:
            download_song(song, target_dir)
    elif mode == 'mv':
        if len(sys.argv) < 5:
            exit('Not enough arguments')
        mv_id = str(sys.argv[3])
        mv_json = get_mv_info(mv_id)
        if mv_json == None:
            print("Get mv contents failed")
            exit()
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        clarity = sys.argv[4]
        download_mv(mv_json, target_dir, clarity)
    elif mode == 'test':
        print('haha, No IndentationError')
    


    
