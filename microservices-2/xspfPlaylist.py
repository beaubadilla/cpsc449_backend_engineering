import sys
import os
import flask_api
from flask import request, send_file
from flask_api import status, exceptions
import pugsql
import xspf
import requests


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Available endpoints: </h1><h2>Make a playlist: </h2><ol><li><a href="/api/v1/makeplaylist/1">Generate playlist xspf with playlist id</a></li></ol>'''

@app.route('/api/v1/makeplaylist/<int:id>', methods=['GET'])
def makeplaylist(id):
    #TODO: change to universal endpoint
    # make a get request for the playlist with given playlist id
    r = requests.get('http://localhost:8000/api/v1/playlists?id='+str(id))
    if r.status_code == 200:
        r = r.json()
        # all info will be added onto this
        x = xspf.Xspf()
        #TODO: change to universal endpoint
        # request user info and check if it went through to get the
        userInfo = requests.get('http://localhost:8000/api/v1/users/'+str(r[0]['UserId']))
        if userInfo.status_code == 200:
                userInfo = userInfo.json()
                x.creator = userInfo['Display_name']
                x.info = userInfo['Homepage_url']

        x.title = r[0]['PLaylistName']

        # add tracks one by one, requesting
            # from endpoint: tracks and Track Descriptions
        for track in r:
            #TODO: change to universal endpoint
            # get tracks
            t = requests.get('http://localhost:8000/api/v1/tracks?id='+str(track['TrackId'])).json()
            trackDesc = requests.get('http://localhost:8000/api/v1/users/'+str(track['UserId'])+'/tracks/'+str(track['TrackId'])+'/descriptions')

            #TODO: change to universal endpoint
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
            x.add_track(tr1)

        # make a filename to store the xml
            # using playlist title with spaces being replaced with '_'
        fileName = x.title + '.xspf'
        # make the file, and since the xml is rendered in bytes,
            # will have to store it as b, so "wb"
        fileName = fileName.replace(' ', '_')
        f = open('Playlists/' + fileName, "wb")
        f.write(x.toXml())
        f.close()
        try:
            return send_file(os.path.join('Playlists', fileName), as_attachment=True)
        except Exception as e:
            return str(e)
    else:
        return {"info": "Does not exist"}, r.status_code
