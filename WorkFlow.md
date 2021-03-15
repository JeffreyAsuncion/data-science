
# data-scienceto Run flask app
pipenv shell
export FLASK_APP=beats:APP
flask run




# installs for pipenv
pipenv install flask FLASK-SQLAlchemy
pipenv install spotipy 
pipenv install python-dotenv
pipenv install plotly
pip install spotipy --upgrade
pipenv install python-dotenv
pipenv install simplejson
pipenv install  flask-cors
pipenv install plotly
pipenv install sklearn





# https://flask-cors.readthedocs.io/en/latest/

# https://spotipy.readthedocs.io/en/2.13.0/


>>> from beats.db_model import db, Song
>>> db.init_app(app)
>>> db.create_all()
>>> db #<SQLAlchemy engine=sqlite:///C:\Users\jeffr\mystuff\data-science\beats\song.sqlite3>
>>> Song #<class 'beats.db_model.Song'>
>>> Song.query.filter_by(Song.id=='6llUzeoGSQ53W3ThFbReE2').all() # gives all db


# this is the code to get info
>>> Song.query.get('6llUzeoGSQ53W3ThFbReE2')
< Title  'Young and Fine' - Artist  "['Weather Report']" - Duration(ms) 413587.0 >

# note one feature from radar Plots is missing
['danceability',  'instrumentalness', 'loudness', 'speechiness',  'valence'] 


>>> Song.query.get('6llUzeoGSQ53W3ThFbReE2')
< Title  'Young and Fine' - Artist  "['Weather Report']" - Duration(ms) 413587.0 - A - 0.725 - D  0.371 - I 0.000139 - L -9.952 - S 0.0488 - V 0.6729999999999999 >



heroku adding postgre db

heroku dashboard
overview
configure add-ons
Add-ons - find box type Heroku Postgres
Plan name Hobby Dev - Free
click Provision

or anaconda heroku cli
ctrl c
heroku addons:create heroku-postgresql:hobby-dev

back to heroku dashboard
click on heroku postgre - attached as database
info how to connect to the heroku postgres
limit 10,000 rows
setting tab for db creds

back to main dashboard 
setting
config vars - DATABASE_URL  postgres://????????? is there for app



check twitoff reset route
create etl route

1:38:04

# help stack overflow you're our only hope
 pip freeze > requirement.txt

# must be requirements.txt not the above output

# what is a CORS Error 
we fixed it with 3 lines of CORS code
CORS error 



two changes sqlite closed
open reset


mission no database just hit api for all data