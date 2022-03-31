from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey as FastApiKey, APIKeyHeader
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN

from feeds.atom_feed import LatestAtomFeed
from feeds.rss_feed import LatestRssFeed
from sql_app.models import movie_model, api_key_model
from sql_app.repositories.api_key_repository import ApiKeyRepo
from sql_app.repositories.movie_repository import MovieRepo
from sql_app.schemas.api_key_schema import ApiKey, ApiKeyCreate, ApiDomain
from sql_app.schemas.movie_schema import Movie, MovieCreate
from sqlite_db.sqlite import engine, get_db

app = FastAPI(title="Movie API Server",
              description="get more deep info about movies.",
              debug=True
              )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

movie_model.Base.metadata.create_all(bind=engine)
api_key_model.Base.metadata.create_all(bind=engine)
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def validate_public_key(api_token: str = Security(api_key_header)):
    if api_token:
        return api_token
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="No authorization found"
        )


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Execution Failed: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.get('/', tags=["home"], response_model=List[Movie])
def home(db: Session = Depends(get_db)):
    MovieRepo.fetch_all(db)


@app.get('/feeds/rss', tags=["rss"], response_model=List[Movie])
def get_rss_feeds(db: Session = Depends(get_db)):
    rss = LatestRssFeed(title="Hey", price=34.00, description="hello Again", link="")
    return rss.items(db)


@app.get('/feeds/atom', tags=["atom"], response_model=List[Movie])
def get_atom_feeds(db: Session = Depends(get_db)):
    rss = LatestAtomFeed(title="Hey", subtitle="What happened", price=34.00, description="hello Again", link="")
    return rss.items(db)


@app.post('/movies', tags=["Movie"], response_model=Movie, status_code=201)
async def create_movie(
        movie_request: MovieCreate,
        api_key: FastApiKey = Depends(validate_public_key),
        db: Session = Depends(get_db)
) -> dict:
    """
    Create a movie and store it in the database
    """
    db_existing_key = ApiKeyRepo.fetch_by_public(db, api_key[7:])
    if db_existing_key:
        db_movie = MovieRepo.fetch_by_title_and_subtitle(db, title=movie_request.title, subtitle=movie_request.subtitle)
        if db_movie:
            raise HTTPException(status_code=400, detail="Movie already exists!")
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    return await MovieRepo.create(db, movie=movie_request)


@app.get('/movies', tags=["Movie"], response_model=List[Movie])
def get_all_movies(db: Session = Depends(get_db), title: Optional[str] = None):
    """
    Get all the Items stored in database
    """
    if title:
        movies = []
        db_movie = MovieRepo.fetch_by_title(db, title)
        movies.append(db_movie)
        return movies
    else:
        return MovieRepo.fetch_all(db)


@app.get('/movies/{movie_id}', tags=["Movie"], response_model=Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_movie = MovieRepo.fetch_movie_by_id(db, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found with the given ID")
    return db_movie


@app.delete('/movies/{movie_id}', tags=["Movie"])
async def delete_movie(movie_id: int,
                       db: Session = Depends(get_db),
                       api_key: FastApiKey = Depends(validate_public_key)):
    """
    Delete the movie with the given ID provided by User stored in database
    """
    db_existing_key = ApiKeyRepo.fetch_by_public(db, api_key)
    if db_existing_key:
        db_movie = MovieRepo.fetch_movie_by_id(db, movie_id)
        if db_movie is None:
            raise HTTPException(status_code=404, detail="Movie not found with the given ID")
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    await MovieRepo.delete(db, movie_id)
    return "Movie deleted successfully!"


@app.put('/movies/{movie_id}', tags=["Movie"], response_model=Movie)
async def update_movie(movie_id: int,
                       movie_request: Movie,
                       db: Session = Depends(get_db),
                       api_key: FastApiKey = Depends(validate_public_key)):
    """
    Update a movie saved in the database
    """
    db_existing_key = ApiKeyRepo.fetch_by_public(db, api_key)
    if db_existing_key:
        db_movie = MovieRepo.fetch_movie_by_id(db, movie_id)
        if db_movie:
            update_movie_encoded = jsonable_encoder(movie_request)
            db_movie.title = update_movie_encoded['title']
            db_movie.subtitle = update_movie_encoded['subtitle']
            db_movie.price = update_movie_encoded['price']
            db_movie.description = update_movie_encoded['description']
            return await MovieRepo.update(db, movie_data=db_movie)
        else:
            raise HTTPException(status_code=400, detail="Movie not found with the given ID")
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.post('/keys', tags=["ApiKey"], response_model=ApiKey, status_code=201)
async def create_api_key(key_request: ApiKeyCreate, db: Session = Depends(get_db)):
    """
    Create api keys and store it in the database
    """
    is_secret_key_unique = False
    is_public_key_unique = False
    secret_key = ''
    public_key = ''
    db_key = ApiKeyRepo.fetch_by_domain(db, domain=key_request.domain)
    if db_key:
        raise HTTPException(status_code=400, detail="Domain already exists!")

    while is_secret_key_unique is False and is_public_key_unique is False:
        if is_secret_key_unique is not True:
            secret_key = ApiKeyRepo.generate_secret_key()
            db_existing_secret = ApiKeyRepo.fetch_by_secret(db, secret=secret_key)
            if db_existing_secret is None:
                is_secret_key_unique = True
        if is_public_key_unique is not True:
            public_key = ApiKeyRepo.generate_public_key()
            db_existing_public = ApiKeyRepo.fetch_by_public(db, public=public_key)
            if db_existing_public is None:
                is_public_key_unique = True
    key_request.secret = secret_key
    key_request.public = public_key
    return await ApiKeyRepo.create(db, api_key=key_request)


@app.get('/keys/{key_id}', tags=["ApiKey"], response_model=ApiKey)
def get_key(key_id: int,
            db: Session = Depends(get_db),
            api_key: FastApiKey = Depends(validate_public_key)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_existing_key = ApiKeyRepo.fetch_by_public(db, api_key)
    if db_existing_key:
        db_key = ApiKeyRepo.fetch_api_key_by_id(db, key_id)
        if db_key is None:
            raise HTTPException(status_code=404, detail="Key not found with the given ID")
        return db_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.get('/keys/{domain}', tags=["ApiDomain"], response_model=ApiDomain)
def get_key_using_domain(domain: str,
                         db: Session = Depends(get_db),
                         api_key: FastApiKey = Depends(validate_public_key)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_existing_key = ApiKeyRepo.fetch_by_public(db, api_key)
    if db_existing_key:
        db_key = ApiKeyRepo.fetch_by_domain(db, domain)
        if db_key is None:
            raise HTTPException(status_code=404, detail="Key not found with the given domain")
        return db_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.delete('/keys/{domain}', tags=["ApiKey"])
async def delete_key(domain: str,
                     db: Session = Depends(get_db),
                     api_key: FastApiKey = Depends(validate_public_key)):
    """
    Delete the key with the given domain provided by User stored in database
    """
    db_existing_key = ApiKeyRepo.fetch_by_public(db, api_key)
    if db_existing_key:
        db_key = ApiKeyRepo.fetch_by_domain(db, domain)
        if db_key is None:
            raise HTTPException(status_code=404, detail="Key not found with the given domain")
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    await ApiKeyRepo.delete(db, domain)
    return "Key deleted successfully!"


@app.put('/keys/{domain}', tags=["ApiKey"], response_model=ApiDomain)
async def update_key(domain: int, key_request: ApiKey, db: Session = Depends(get_db)):
    """
    Update a key stored in the database
    """
    db_key = ApiKeyRepo.fetch_by_domain(db, domain)
    if db_key:
        update_movie_encoded = jsonable_encoder(key_request)
        db_key.secret = update_movie_encoded['title']
        db_key.public = update_movie_encoded['subtitle']
        return await ApiKeyRepo.update(db, api_key_data=db_key)
    else:
        raise HTTPException(status_code=400, detail="Key not found with the given domain")


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
