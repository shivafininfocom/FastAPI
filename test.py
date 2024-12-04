import requests
import json
symbol = 'AAPL'
api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
response = requests.get(api_url, headers={'X-Api-Key': 'PrlkE5ycgmID0DxvnZOJqg==wvOez5JYIn1jyxGF'})
if response.status_code == requests.codes.ok:
    print(response.text)
    apple_share = response.json()
    print(json.loads(apple_share))
else:
    print("Error:", response.status_code, response.text)