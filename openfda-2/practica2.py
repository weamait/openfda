import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection('api.fda.gov')
conn.request('GET', '/drug/label.json?&search=active_ingredient:"acetylsalicylic+acid"&limit=100', None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

for elem in repos['results']:
    if elem['openfda']:
        print("Nombre de fabricante que produce aspirinas:", elem['openfda']['manufacturer_name'])
    else:
        continue