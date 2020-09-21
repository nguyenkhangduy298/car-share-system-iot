import requests
# res = requests.get('http://localhost:5000/report')
# res2 = requests.post('http://localhost:5000/create', json={"temperature":"36","humidity":"40"})
res3 = requests.get('http://localhost:5000/customer')

if res3.ok:
    print (res3.json())