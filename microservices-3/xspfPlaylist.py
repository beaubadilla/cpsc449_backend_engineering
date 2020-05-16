import sys
import os
import flask_api
from flask import request, send_file
from flask_api import status, exceptions
import pugsql
import xspf
import requests
from pymemcache.client import base
import json


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

client = base.Client(('localhost', 11211))

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Available endpoints: </h1><h2>Make a playlist: </h2><ol><li><a href="/api/v1/makeplaylist/1">Generate playlist xspf with playlist id</a></li></ol>'''

@app.route('/api/v1/makeplaylist/<int:id>', methods=['GET'])
def makeplaylist(id):
    # Check cache for playlist
    result = client.get(str(id))
    # If cache value exists
    if result is not None:
        print(result)
        result = result.decode('utf-8')
        result = result.replace("\'", "\"")
        # result = json.dumps(result)
        result = json.loads(result)
        print(result)

            # construct XSPF repsonse
        x = xspf.Xspf()
        x.creator = result['Display_name']
        x.info = result['Homepage_url']
        x.title = result['PLaylistName']
        for track in result['Tracks']:
            a_track = xspf.Track()
            a_track.info = 'http://localhost:8000/api/v1/playlists?id='+str(id)
            a_track.title = track['TrackName']
            a_track.album = track['Album']
            a_track.duration = str(track['Length'])
            a_track.location = track['Url']
            a_track.image = track['Art']
            a_track.creator = track['Artist']
            try:
                a_track.annotation = track['Comment']
            except Exception as e:
                a_track.annotation = ""
            x.add_track(a_track)
        fileName = x.title + '.xspf'
        fileName = fileName.replace(' ', '_')
        f = open('Playlists/' + fileName, "wb")
        f.write(x.toXml())
        f.close()
        try:
            return send_file(os.path.join('Playlists', fileName), as_attachment=True)
        except Exception as e:
            return str(e)

    # If cache value does not exist
    elif result is None:
        #TODO: change to universal endpoint
        # make a get request for the playlist with given playlist id
        r = requests.get('http://localhost:5200/api/v1/playlists?id='+str(id))
        if r.status_code == 200:
            json_obj = {"Tracks": []}
            r = r.json()
            # all info will be added onto this
            x = xspf.Xspf()
            #TODO: change to universal endpoint
            # request user info and check if it went through to get the
            userInfo = requests.get('http://localhost:5000/api/v1/users/'+str(r[0]['UserId']))
            if userInfo.status_code == 200:
                    userInfo = userInfo.json()
                    x.creator = userInfo['Display_name']
                    x.info = userInfo['Homepage_url']
                    json_obj["Display_name"] = userInfo['Display_name']
                    json_obj["Homepage_url"] = "userInfo[Homepage_url]"

            x.title = r[0]['PLaylistName']
            json_obj["PLaylistName"] = r[0]['PLaylistName']
            # add tracks one by one, requesting
                # from endpoint: tracks and Track Descriptions
            for track in r:

                #TODO: change to universal endpoint
                # get tracks
                t = requests.get('http://localhost:5300/api/v1/tracks?id='+str(track['TrackId'])).json()
                trackDesc = requests.get('http://localhost:5100/api/v1/users/'+str(track['UserId'])+'/tracks/'+str(track['TrackId'])+'/descriptions')

                #TODO: change to universal endpoint
                t = {
                "TrackName": t['TrackName'],
                "Album": t['Album'],
                "Length": str(t['Length']),
                "Url": t['Url'],
                "Art": t['Art'],
                "Artist": t['Artist'],
                "Comment": ""
                }
                tr1 = xspf.Track()
                tr1.info = 'http://localhost:8000/api/v1/playlists?id='+str(id)
                tr1.title = t['TrackName']
                tr1.album = t['Album']
                tr1.duration=str(t['Length'])
                tr1.location=t['Url']
                tr1.image=t['Art']
                tr1.creator=t['Artist']
                if trackDesc.status_code == 200:
                    trackDesc = trackDesc.json()
                    tr1.annotation = trackDesc['Comment']
                    t["Comment"] = trackDesc['Comment']

                x.add_track(tr1)
                # tr = merge(t, trackDesc)
                json_obj["Tracks"].append(t)

            # make a filename to store the xml
                # using playlist title with spaces being replaced with '_'
            fileName = x.title + '.xspf'
            # make the file, and since the xml is rendered in bytes,
                # will have to store it as b, so "wb"
            fileName = fileName.replace(' ', '_')
            f = open('Playlists/' + fileName, "wb")
            f.write(x.toXml())
            f.close()

            client.set(str(id), json_obj)
            try:
                return send_file(os.path.join('Playlists', fileName), as_attachment=True)
            except Exception as e:
                return str(e)
        else:
            return {"info": "Does not exist"}, r.status_code
