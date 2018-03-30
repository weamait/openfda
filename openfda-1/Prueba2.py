import json
import urllib.request


url = 'https://api.fda.gov/drug/label.json?&limit=11'
req = urllib.request.Request(url)

r = urllib.request.urlopen(req).read()
cont = json.loads(r.decode('utf-8'))

for item in cont['results']:
    print("El identificador es:", item['id'])


import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=11", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

for elem in repos['results']:
    print("El identificador es:", elem['id'])