# URL Shortener API

A simple URL Shortener built using FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication.

## Features

* User Authentication (JWT)
* Create Short URLs
* Custom URL Aliases
* Redirect to Original URLs
* URL Expiration (90 Days)
* Click Count Tracking

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* ShortUUID

## Endpoints

### Authentication

* `POST /register`
* `POST /login`

### URL Management

* `POST /short_url` → Create short URL
* `POST /short_url/{custom_code}` → Create custom alias
* `GET /short_url/{code}` → Redirect to original URL
* `GET /short_url/exp/{code}` → Check expiration date

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

## Future Improvments
* QR code Generation
* Admin level Authantication
* Full Fuctional User Dashboard

# Author
   BALMUKUND PANDEY
