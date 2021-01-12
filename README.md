# API Benchmark

Benchmarking three Python API frameworks based on simple image processing task

## Frameworks:
- [x] FlaskAPI
- [x] FastAPI
- [x] aioHTTP


## How to run

### Flask API

#### Server side
    uvicorn app:app --reload       # --reload to automatically reflect code changes

    uvicorn app:app --reload --log-level critical  # to suppress the console log


#### Client side
    python flask_client.py
    pytest


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
   

    locust -f locustfile.py --headless --host http://127.0.0.1:5000 -u 2000 -r 50 -t 30s --csv reports/imageurl_${i} ImageUrlUser
    locust -f locustfile.py --headless --host http://127.0.0.1:5000 -u 2000 -r 50 -t 30s --csv reports/base64_${i} Base64User
    locust -f locustfile.py --headless --host http://127.0.0.1:5000 -u 2000 -r 50 -t 30s --csv reports/multipart_${i} MultipartUser

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

all APIs were tested for performance using wrk HTTP benchmarking tool. 
wrk tool is based on C and requires in-depth knowledge of Lua to pass the base64 encoded images as multipart/data. 
Hence, I switched to locust, which is a python based HTTP benchmarking tool. It made the task very much easier since it utilizes the same request library like the client. However, it should be noted that wrk is extremely fast compared to locust.

Parameters for load testing:

- Number of users = 2000

- User spawning rate = 50/second

- Duration of test = 30s


## Results


![Latency](/assets/latency.png)


![Request/Second](/assets/request_per_second.png)


![Content Size](/assets/content_size.png)


![Request Count](/assets/request_count.png)
 
