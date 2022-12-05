import requests

HOST = 'http://127.0.0.1:5000'

# response = requests.post(f'{HOST}/ads/',json={'article':'hi1hi','text':'ertert','owner':'ertert'})
response = requests.get(f'{HOST}/ads/1')
# response = requests.patch(f'{HOST}/ads/1',json={'article':'try patch'})
# response = requests.delete(f'{HOST}/ads/2')

print(response.status_code)