
# encoding:utf-8
import requests 

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=BmN5LlqTWvH09M4PN0NZt3EN&client_secret=i9abTNIKvqKSK2g6h2HuKkdtYxAYIjEu'
response = requests.get(host)
if response:
    print(response.json())