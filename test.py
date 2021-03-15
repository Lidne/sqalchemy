import requests

some = requests.get('http://127.0.0.1:5000/api/news').json()
print(some)