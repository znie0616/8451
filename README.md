# 8451

* requires pipenv installed

I generated a 10 by 10 board filled with letter A-Z or empty string with following command: 
pipenv run python board_generator.py 10

run ReST service with:
pipenv run python endpoint.py

- health check: localhost:/8451/health
- words search GET request (takes one query param which is a list of words or one word to search, comma separated, case insensitive): 
localhost:/8451?words=abc,cde

test file under test/, run with:
pipenv run pytest test_endpoint.py -v
