import requests

url = 'http://127.0.0.1:3000/register'
datas = {
    'username': 'limo1029',
    'Email': '1282160815@qq.com',
    'pwd': '20041123'
}
while True:
    print(requests.post(url, datas).json())
