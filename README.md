# http-server
This program builds an echo server. Ultimately, the client will send an HTTP request to the server, which will return an HTTP status response. 

Our server.py has functions to forumulate these responses, which can be called in the main server() function- *response_ok()*, which returns a HTTP/1.1 200 OK status when called,.

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
src/client.py            31      6    81%   42-46, 50
src/server.py            39     21    46%   13-42, 63
src/test_servers.py      19      1    95%   29
---------------------------------------------------
TOTAL                    89     28    69%


=============================================== 6 passed in 0.04 seconds

---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            31      8    74%   20-21, 42-46, 50
src/server.py            39     23    41%   13-42, 49, 57, 63
src/test_servers.py      19      1    95%   27
---------------------------------------------------
TOTAL                    89     32    64%


=============================================== 6 passed in 0.09 seconds 
_______________________________________________________ summary ___________
```
