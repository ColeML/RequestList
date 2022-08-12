# RequestList

## Python3 Flask application that is used to track wanted media.
Flask API
Flask-JWT-Extended
React Frontend
PostgreSQL Database
Redis
Deployed on Heroku

## Features
### Movie Requests
Look up Movies using the omdb api.
Requests are made using the imdb_id of the wanted movie.

### Show Requests
Looks up Shows using the omdb api.
Requests are made using the imdb_id of the wanted show.

### Book Requests
Looks up Books using the Google books api.
Requests are made using the isbn10 or isbn13 of the wanted book.
Supports ebooks and audiobooks.

### Music Requests
Looks up Music using the Deezer api.
Requests are made using the deezer_id of the wanted music.
Supports albums and tracks.


## TODO List:
* Implement Email notifications
* Implement Functional Tests
* Implement Unit Tests
* Implement Simple Front End
* Docker Build
* Look into different api for Movies and TV Shows (without daily limit)

## Possible Ideas List
* Multiple APIs per lookup for more uncommon media
