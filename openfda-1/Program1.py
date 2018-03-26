import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

repo = repos['results']
print("El identificador es", repo[0]['id'], ", el propósito es", repo[0]['purpose'], "y el nombre del fabricante es",repo[0]['openfda']['manufacturer_name'])
