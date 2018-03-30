import json
import urllib.request


url = 'https://api.fda.gov/drug/label.json?&limit=11'
req = urllib.request.Request(url)

r = urllib.request.urlopen(req).read()
cont = json.loads(r.decode('utf-8'))

for item in cont['results']:
    print("El identificador es:", item['id'])