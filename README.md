# http-server
This program builds an echo server. Ultimately, the client will send an HTTP request to the server, which will return an HTTP status response. 

Our server.py has three functions to forumulate these responses, which can be called in the main server() function- *response_ok()*, which returns a HTTP/1.1 200 OK status when called, and *response_error(code)*, which returns a HTTP/1.1 Error when called with a code number, and *parse_request(header)* which takes a header message sent from the client and returns the uri.

##Modules:
1. client.py
2. server.py

##Test Modules:
1. test_servers.py


#Testing Coverage:
```
---------- coverage: platform darwin, python 2.7.11-final-0 ----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            30      6    80%   40-44, 48
src/server.py            66     32    52%   12-53, 110
src/test_servers.py      23      0   100%
---------------------------------------------------
TOTAL                   119     38    68%


============================================= 11 passed in 0.07 seconds =



---------- coverage: platform darwin, python 3.5.2-final-0 -----------
---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            30      8    73%   19-20, 40-44, 48
src/server.py            66     34    48%   12-53, 60, 77, 110
src/test_servers.py      23      0   100%
---------------------------------------------------
TOTAL                   119     42    65%
```
