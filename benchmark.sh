#!/bin/bash

for i in {1..5}
  do
    echo "----------------------   RUN ${i}    -------------------------"
    wrk http://127.0.0.1:5000/magic -t12 -c400 -d30s -s lua_scripts/post.lua
    echo -e "\n"
  done
echo All done

