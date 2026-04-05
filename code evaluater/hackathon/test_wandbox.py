import urllib.request
import json

data = json.dumps({'code': 'print("hello")', 'compiler': 'cpython-head'}).encode()
req = urllib.request.Request('https://wandbox.org/api/compile.json', data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print(e)
