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

def save_file(var, url, file_name):
    if os.path.isfile(file_name):
        print('%s already existed.' % var)
    else:
        print('downloading...%s' % var)
        url_content = requests.get(url).content 
        with open(file_name, 'wb') as f:
            f.write(url_content)
            print('%s saved' % var)

def download_songid(songid, target_dir):
    url = 'http://music.163.com/api/song/detail/?id=' + songid + '&ids=[' + songid +']'
    res = get_json(url)
    songs = res['songs'][0]
    
    song = {
            'name' : songs['name'].replace('/', ''),
            'songid' : songid,
            'artists' : mk_artists(songs)
        }
    download_song(song, target_dir)

def download_song(song, target_dir):
    print("\nSongid: %s, name: %s, artists: %s" % (song['songid'], song['name'], song['artists']))
    song_url = 'http://music.163.com/song/media/outer/url?id=' + song['songid']
    file_name = "%s\\%s-%s.mp3" % (target_dir, song['name'], song['artists'])
    save_file('Music', song_url, file_name)

def download_playlist(playlist, target_dir):
    print("Get msg from playlist: %s" % playlist)
    url = 'http://music.163.com/api/playlist/detail?id=' + playlist
    playlist_json = get_json(url)
    if playlist_json == None:
        print("Get songlist contents failed")
        exit()

    tracks_arr = playlist_json['result']['tracks']
    for track in tracks_arr:
        song = {
            'name' : track['name'].replace('/', ''),
            'songid' : str(track['id']),
            'artists' : mk_artists(track)
            }
        download_song(song, target_dir)

def download_mv(mv_id, target_dir, clarity):
    clarities = ['240', '480', '720', '1080']
    if clarity not in clarities:
        clarity = 1080
        print('automate select, clarity = 1080')
        
    url = 'http://music.163.com/api/mv/detail?id=%s' % mv_id
    mv_json = get_json(url)
    if mv_json == None:
        print("Get mv contents failed")
        exit()
    
    data = mv_json['data']
    name = data['name']
    artists = mk_artists(data)

    print("\nMV id: %s, name: %s, artists: %s" % (mv_id, name, artists))
    cover_url = data['cover']
    cover = "%s\\%s-%s.jpg" % (target_dir, name, artists)
    save_file('Cover', cover_url, cover)
    
    video_url = data['brs'][clarity]
    video = "%s\\%s-%s.mp4" % (target_dir, name, artists)
    save_file('Video', video_url, video)   
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        exit('Not enough arguments')
    mode = sys.argv[1]
    target_dir = sys.argv[2]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    if mode == 'song':
        songid = str(sys.argv[3])
        download_songid(songid, target_dir)
    elif mode == 'playlist':
        playlist = sys.argv[3]
        download_playlist(playlist, target_dir)
    elif mode == 'mv':
        if len(sys.argv) < 5:
            exit('Not enough arguments')
        mv_id = str(sys.argv[3])
        clarity = sys.argv[4]
        download_mv(mv_id, target_dir, clarity)
    elif mode == 'test':
        print('haha, No IndentationError')
    


    
