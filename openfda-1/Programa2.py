import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?search=results.openfda:spl_id&limit=1", None, headers)
id0 = conn.getresponse()
for elem in id0:
    print(elem)