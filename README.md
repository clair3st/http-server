# http-server
This program builds an echo server. Ultimately, the client will send an HTTP request to the server, which will return an HTTP status response. 

Our server.py has two functions to forumulate these responses, which can be called in the main server() function- *response_ok()*, which returns a HTTP/1.1 200 OK status when called, and *response_error()*, which returns a HTTP/1.1 500 Internal Server Error when called.

##Modules:
1. client.py
2. server.py

##Test Modules:
1. test_servers.py


#Testing Coverage:
```
================ 2 passed in 0.03 seconds ===============

----- coverage: platform darwin, python 2.7.10-final-0 -----
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            30     30     0%   3-48
src/server.py            40     23    43%   11-45, 67
src/test_servers.py       8      0   100%
---------------------------------------------------
TOTAL                    78     53    32%



------ coverage: platform darwin, python 3.5.2-final-0 ------

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            30     30     0%   3-48
src/server.py            40     25    38%   11-45, 52, 61, 67
src/test_servers.py       8      0   100%
---------------------------------------------------
TOTAL                    78     55    29%
```
