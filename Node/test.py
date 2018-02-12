import requests as r
import json

a = r.get("http://localhost:5555/pending_transactions")

headers = {'content-type': 'application/json'}
url = "http://localhost:5555/give_me_beer"
data={"minerAddress" : "torbalan"}

b = r.post(url, data=json.dumps(data), headers=headers)



print(a.content.decode())
print(b.content.decode())


