-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "GET"
wrk.body   = "{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"
wrk.headers["Content-Type"] = "application/json"
