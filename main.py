import os
import requests

url1 = "http://localhost:5000/create_delivery_request"
url2 = "http://localhost:5000/get_delivery_info?id=2"
url3 = "http://localhost:5000/delete_delivery?id=2"
url4 = "http://localhost:5000/change_delivery_status"

data = {
    'sender_name': 'Roman',
    'sender_address': 'Moscow',
    'getter_name': 'Oleg',
    'getter_address': 'Ekaterinburg',
    'info': 'Phone'
}
data1 = {
    'id': '2',
    'status': 'in delivery'
}

response = requests.delete(url3)

print(response.json(), response.status_code)