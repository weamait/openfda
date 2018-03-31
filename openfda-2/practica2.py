import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&search=active_ingredient:%22acetylsalicylic+acid%22&limit=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

for elem in repos['results']:
    print("Los nombres de todos los fabricantes que producen aspirinas son:", elem['openfda']['manufacturer_name'])