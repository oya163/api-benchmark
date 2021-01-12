#!/bin/bash

for i in {1..5}
  do
    echo "----------------------   RUN ${i}    -------------------------"
#    wrk http://127.0.0.1:5000/magic/base64 -t12 -c400 -d30s -s lua_scripts/post.lua
    locust -f locustfile.py --headless --host http://127.0.0.1:5000 -u 5000 -r 100 -t 30s --csv reports/imageurl_${i} ImageUrlUser
    echo -e "\n"
  done
echo All done

