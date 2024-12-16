import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

playlist_id = '1o6MAdcyrGWxcAVj0Bp3vF'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#in minutes
cassettePlayTime = 90

results = spotify.playlist_items(playlist_id)

with open('export.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["Track Number", "Song Name","Artist","Album","Duration"]
    writer.writerow(field)
    runningDuration = 0
    trackCount = 0
    aSideTotal = -1
    bDurationRemaining = cassettePlayTime/2*60*1000
    for track in results["items"]:
        artist = (track["track"]["artists"][0]["name"])
        trackName = (track["track"]["name"])
        albumName = (track["track"]["album"]["name"])
        durationms = track["track"]["duration_ms"]
        seconds=(durationms/1000)%60
        seconds = int(seconds)
        minutes=(durationms/(1000*60))%60
        minutes = int(minutes) 
        duration = ("%d:%d" % (minutes, seconds))
        runningDuration += durationms
        trackCount +=1
        if (runningDuration<cassettePlayTime/2*60*1000):
            trackNum = "A"+str(trackCount)
            aSideTotal+=1
        else:
            trackNum="B"+str(trackCount-aSideTotal)
            bDurationRemaining-=durationms
        writer.writerow([trackNum,trackName,artist,albumName,duration])
        if (bDurationRemaining<0):
            print(trackName +" would run over your total time limit")
            break
print(runningDuration)