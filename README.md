# API Benchmark

This project is about benchmarking three different Python API frameworks based on simple image processing task. The basic concept is the APIs consumes either image file in the form of base64 encoding or multipart-data or just a image url, and returns the corresponding pure black and white image to the client.

## Frameworks:
- [x] [FlaskAPI](https://flask-restful.readthedocs.io/en/latest/)
- [x] [FastAPI](https://fastapi.tiangolo.com/)
- [x] [aioHTTP](https://docs.aiohttp.org/en/stable/)


## How to run

### Flask API

#### Server side
    uvicorn app:app --reload       # --reload to automatically reflect code changes

    uvicorn app:app --reload --log-level critical  # to suppress the console log


#### Client side
    python flask_client.py
    pytest

### Jinja
Once you run the server, please goto [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
in order to check the results visually. This API server retrieves random dog images
using [Dog API](https://dog.ceo/dog-api/) and converts it into pure black and white.

### Fast API

#### Server side
    uvicorn app:app --reload       # --reload to automatically reflect code changes

    uvicorn app:app --reload --log-level critical  # to suppress the console log


#### Client side
    python fast_client.py
    pytest


### aioHTTP

#### Server side
    python -m app.py -H localhost -P 8000 package.module:init_func


#### Client side
    python client_aiohttp.py
    pytest


## Benchmarking
1. [locust](https://locust.io/)
   

        locust -f locustfile.py --headless --host http://127.0.0.1:5000 -u 2000 -r 50 -t 30s --csv reports/imageurl ImageUrlUser
        locust -f locustfile.py --headless --host http://127.0.0.1:5000 -u 2000 -r 50 -t 30s --csv reports/base64 Base64User
        locust -f locustfile.py --headless --host http://127.0.0.1:5000 -u 2000 -r 50 -t 30s --csv reports/multipart MultipartUser

or, just run `./benchmark.sh` for 5-trial run

2. [wrk](https://github.com/wg/wrk)

*Note: This currently works for `imageurl` endpoint only*

- Flask API


        wrk http://127.0.0.1:5000/magic/imageurl -t12 -c400 -d30s -s lua_scripts/post.lua

- Fast API


        wrk http://127.0.0.1:8000/magic/imageurl -t12 -c400 -d30s -s lua_scripts/post.lua

- aioHTTP


        wrk http://0.0.0.0:8080/magic/imageurl -t12 -c400 -d30s -s lua_scripts/post_aiohttp.lua

## Experiments

Initially, aLL API endpoints were tested for performance using **wrk** HTTP benchmarking tool. 
**wrk** tool is based on C and requires in-depth knowledge of Lua to pass the base64 encoded images as multipart/data. I faced great difficulty in passing base64 encoding image or multipart/form-data as a payload through **wrk**. Hence, I switched to **locust**, which is a python based HTTP benchmarking tool. It made the task very much easier since it utilizes the `requests` library. However, it should be noted that **wrk** is extremely fast compared to locust.

Parameters for load testing on *locust**:

- Number of users = 2000

- User spawning rate = 50/second

- Duration of test = 30s


## Results


![Latency](/assets/latency.png)


![Request/Second](/assets/request_per_second.png)


![Content Size](/assets/content_size.png)


![Request Count](/assets/request_count.png)
 
