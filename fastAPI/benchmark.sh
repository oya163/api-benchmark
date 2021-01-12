#!/bin/bash

#for i in {1..5}
#  do
#    echo "----------------------   RUN ${i}    -------------------------"
#    locust -f locustfile.py --headless --host http://127.0.0.1:8000 -u 2000 -r 50 -t 30s --csv reports/imageurl_${i} ImageUrlUser
#    echo -e "\n"
#  done
#echo 'Completed ImageUrlUser'

#for i in {1..5}
#  do
#    echo "----------------------   RUN ${i}    -------------------------"
#    locust -f locustfile.py --headless --host http://127.0.0.1:8000 -u 2000 -r 50 -t 30s --csv reports/base64_${i} Base64User
#    echo -e "\n"
#  done
#echo 'Completed Base64User'

for i in {1..5}
  do
    echo "----------------------   RUN ${i}    -------------------------"
    locust -f locustfile.py --headless --host http://127.0.0.1:8000 -u 2000 -r 50 -t 30s --csv reports/multipart_${i} MultipartUser
    echo -e "\n"
  done
echo 'Completed MultipartUser'
