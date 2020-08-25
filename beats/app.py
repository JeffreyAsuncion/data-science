# https://spotipy.readthedocs.io/en/2.13.0/
# pip install spotipy --upgrade
# pipenv install python-dotenv
# pipenv install simplejson
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import time
from flask import Flask, jsonify, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from os import getenv
from dotenv import load_dotenv
# additional
from json.decoder import JSONDecodeError
import json as simplejson
# our json friend
#print(json.dumps(VARIABLE, sort_keys=True, indent=4))



load_dotenv()


# wrap this in a function
market = ["us"]

client_id = getenv('SPOTIPY_CLIENT_ID')
client_secret = getenv('SPOTIPY_CLIENT_SECRET')

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

def create_app():
    '''Create and configure an instance of the Flask application'''

    app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # db.init_app(app)

    @app.route('/hello')
    def hello_world():
        return 'hello'

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/song')
    def getsong():
        '''
        this takes the song name and returns song details
        this takes artist name and returns up to 10 tracks per artist
        '''
        return render_template('asksong.html')

    @app.route('/songinfo', methods=['POST']) #/output changed to songinfo
    def output():
        # User inputs song name here 
        user_input_song = request.form['user_input_song']

        # spotify search params
        results = spotify.search(str(user_input_song), type="track", limit=1)
        return results

    # this route returns more info about an artist
    @app.route('/artistinfo')
    @app.route('/artist/<input_artist>')
    def getartist(input_artist=None):

        input_artist = request.values['input_artist']
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        if input_artist == "":
            return "Can't Touch This! Hammer Time!"
        if "_" in input_artist:
            input_artist = input_artist.replace("_"," ")
        name = input_artist

        ##### This is from LEARN SPOTIFY 6
        # Search of the artist
        
        # Get search results
        searchResults = spotify.search(q='artist:' + name, limit=1, offset=0, type=['artist'])# from LEARN SPOTIFY 5 5:05 added limit=10, offset=0
        print(simplejson.dumps(searchResults, sort_keys=True, indent=4))
        results = simplejson.dumps(searchResults, sort_keys=True, indent=4) #V6T1:12

        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print(artist['images'][0]['url'])
        print()

        return artist
        # TODO return artist just double check format for Front End
        # TODO make this a JSON
        # TODO make this another route and button





    # this route returns a list of up to 10 tracks of a artist
    @app.route('/getsongs')
    @app.route('/getsongsbyartist/<input_artist>')
    def getsonginfo(input_artist=None):

        input_artist = request.values['input_artist']
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        if input_artist == "":
            return "Can't Touch This! Hammer Time!"
        if "_" in input_artist:
            input_artist = input_artist.replace("_"," ")
        name = input_artist

        # Search of the artist
        searchResults = spotify.search(q='artist:' + name, limit=1, offset=0, type=['artist'])
        artist = searchResults['artists']['items'][0]
        artistID = artist['id']
        ##### This is from LEARN SPOTIFY 7

        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotify.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotify.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()
        
        result_string = str(list(zip(trackURIs, trackArt)))

        return result_string
        # return track
        # return results # this works
        # TODO return artist


    @app.route('/songsuggester')
    def feedmodel():
        # User inputs song name here
        user_input_song = request.form['user_input_song']

        # search db for song features
        # twitoff app.py line 30
        ssresult = Song.query(Song.name == user_input_song).one() 
        # NOTE ssresult this is a list       
        
        return ssresults # this should break into name and features





    # the following routes are examples from the link below
    # https://spotipy.readthedocs.io/en/2.13.0/
    # here’s a quick example of using Spotipy to list the names of all the albums released by the artist ‘Birdy’:
    @app.route('/test-1')
    def album_name():
        birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
        # spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

        results = spotify.artist_albums(birdy_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])

        for album in albums:
            print(album['name'])
        return str(albums[0])
        # return render_template('home.html', results=albums['name'])

    #how to get 30 second samples and cover art for the top 10 tracks for Led Zeppelin:
    @app.route('/test-2')
    def top10():
        # URI FOR LED ZEPPELIN
        lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
        results = spotify.artist_top_tracks(lz_uri)

        for track in results['tracks'][:10]:
            print('track    : ' + track['name'])
            print('audio    : ' + track['preview_url'])
            print('cover art: ' + track['album']['images'][0]['url'])
            print()
        # return str(results['tracks'][0]['name']), 
        # results['tracks'][0]['preview_url'], 
        # results['tracks'][0]['album']['images'][0]['url'])
        return str(results['tracks'][0]['name']) +' '+ str(results['tracks'][0]['preview_url']) + ' ' + str(results['tracks'][0]['album']['images'][0]['url'])
    
    



    # TODO: MACHINE LEARNING MODEL FILL - EXAMPLE FROM TWITOFF
    # @app.route('/suggest', methods=['POST'])
    # def compare(message=''):
    #     user1  = request.values['user1']
    #     user2  = request.values['user2']
    #     tweet_text = request.values['tweet_text']

    #     if user1 == user2:
    #         message = 'Cannot compare a user to themselves'
    #     else:
    #         prediction = predict_user(user1, user2, tweet_text)
    #         # message = '"{}" is more likely to be said \nby @{} than @{}'.format(
    #         #     tweet_text, user1 if prediction else user2, user2 if prediction else user1
    #         # )
    #         message = '@{}  is most likely to say "{}" than @{}'.format(
    #             user1 if prediction else user2, tweet_text, user2 if prediction else user1)
    #     # return render_template('prediction.html', title='Prediction', message=message)
    #     return render_template('base.html', title='Prediction', message=message, users=User.query.all())
    return app