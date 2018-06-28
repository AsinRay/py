import requests
headers = {"Authorization": "bb31e154da59f4e0ad6ebe002360dcff78e0afe4"}
r = requests.get('https://api.github.com/user', headers=headers)
# r = requests.get('https://api.github.com/user', auth=('AsinRay', 'xxxxx'))
u = requests.get("https://api.github.com/users/1119264845")
# print(u.json())

r = requests.get('https://api.github.com/search/repositories?q=bitcoin/bitcoin')


# headers = {"Authorization": "bb31e154da59f4e0ad6ebe002360dcff78e0afe4"}
# 前两行会在后面的代码中忽略掉不写
# user = requests.get('https://api.github.com/user', headers=headers).json()
print(r.status_code)
print(r.json())
