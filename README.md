Tinyurl
=======

### Built using Django

This will take any url and create a unique uuid4 ID that is used to referense the full url. This can be thought of as a hash map.

You can see an example of this being used at [smallerlinks.com](www.smallerlinks.com)

Usage
======

Base url endpoint: /api/shorten/


|endpoint|description|method|
|:--------|-----------|------:|
|create/ | create and return a shortened url ID| POST|
|expiration/|get or set the expiration date|GET, POST|
|usage/|get the click count, or increment the click count by one|GET, POST|
|original/|returns the original link this is pointing to|GET|


### Copyright(c) 2017 Joe Berria