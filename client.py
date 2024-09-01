import requests


# response = requests.patch("http://127.0.0.1:5000/advertisement/1/",
#                            json={"name": "dog"})

#
response = requests.delete("http://127.0.0.1:5000/advertisement/1/")

# print(response.status_code)
# print(response.json())
#
# response = requests.get("http://127.0.0.1:5000/advertisement/1/")
#
# print(response.status_code)
# print(response.json())


# response = requests.post(
#     "http://127.0.0.1:5000/advertisement/", json={
#         'name': 'Cat', 'description': 'just a cat', 'owner': 'George'
#     })

print(response.status_code)
print(response.json())
