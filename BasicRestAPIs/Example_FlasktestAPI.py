####related to FlaskRestApi.py file

import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.clear_db(BASE)
# print(response)

data = [{"name": "first vid", "likes": 130, "views": 842},
        {"name": "how to sleep", "likes": 0, "views": 3},
        {"name": "dreaming nice", "likes": 51, "views": 22},
        {"name": "it s too late", "likes": 52, "views": 6432}]

for i in range(len(data)):
    response = requests.put(BASE + f"video/{str(i)}", json=data[i])
    print(response.json())

response = requests.put(BASE + "video/1", json={"name": "first vid", "likes": 10, "views": 1242})
print(response.json())

# response = requests.delete(BASE + "video/2")
# print(response )

response = requests.get(BASE + "video/146")
print(response.json())

response = requests.patch(BASE + "video/2", json={"likes": 777777777})
print(response.json())

response = requests.get(BASE + "video/2")
print(response.json())