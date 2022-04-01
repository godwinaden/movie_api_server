# movie_api_server
A SlashDot Media, Inc. test for the role: Senior Python Engineer.

### Installation
After cloning the app, install virtual environments or pipenv and other dependencies. FastAPI was used in place of Flask
because its performance is higher and can compete with Node and Go. sqlalchemy package was used for ORM 
(Object relational Mapping) for relating with database modeling. sqlite was the database used here for simplicity. 
Uvicorn is an ASGI web server implementation for Python. Uvicorn will be our local server configuration and runtime engine.
            
            pip install pipenv
            pipenv shell
            pipenv install uvicorn
            pipenv install fastapi asyncio[startups] pytest pytest-asyncio
            pipenv install pytest-benchmark requests sqlalchemy pydantic pytest-cov
        
### Debugging / Production
To run the API server, I configured the application to reload automatically on port 9000. so after running the 
application, you can just navigate to http://localhost:9000 from your browser. To see the API server documentations at 
a glance, you can navigate to [http://localhost:9000/docs](http://localhost:9000/docs) or [http://localhost:9000/redoc](http://localhost:9000/redoc)
use the following code to run it.

            python main.py

if your environment is well setup, you will have everything work fine on the browser.

###Testing
To keep the work simple, only few unit test was done using pytest. I intended to use Pytest-benchmark to
measure memory and cpu usage and performance for each method/function but because of time constraints on my part, 
I decided to leave it for another time. I will keep updating this repository in the future to code in other or missing
test cases. To run the test, use the following code:

            python -m pytest test --asyncio-mode=strict --cov
           
###Thanks
Thanks for the patience and the opportunity to carry out this technical test for the role of
Senior Python Engineer. I hope and anticipate taking the role. Thanks again.