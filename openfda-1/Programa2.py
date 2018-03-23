import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.github.com")
conn.request("GET", 'https://api.fda.gov/drug/event.json?search=results:openfda', None, headers)
r1 = conn.getresponse()
print(r1)