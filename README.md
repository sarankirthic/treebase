# treebase
Simple api to create a shorter url

## APIs and features

### /shorten - POST

To create the shorter_url use the following curl command
```curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://example.com"}'```

### /<short_url> - GET

To be redirected to the url page
just paste the url generated in the search bar of the browser to be redirected

## Tech Stack

This project uses python3.11 and Postgresql@14

### Installation

#### Virtualenv Install
```virtualenv venv -p /path/to/python/version```

#### Start Virtualenv
```source venv/bin/activate```

#### Install libraries
```pip install Flask psycopg2-binary SQLAlchemy hashids```

## Usage
Run app.py to start the flask server
