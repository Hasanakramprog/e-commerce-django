# import requests

# url = "https://7103.api.greenapi.com/waInstance7103938518/sendMessage/e33b3980940f40b5abd614cc34a6d867faf9136729524901ae"

# payload = {
# 'chatId': '96170639378@c.us', 
# 'message': 'ddasdas'
# }
# headers = {
# 'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data = payload)

# print(response.text.encode('utf8'))


# import requests

# url = "https://7103.api.greenapi.com/waInstance7103938518/sendMessage/e33b3980940f40b5abd614cc34a6d867faf9136729524901ae"

# payload = "{\r\n\t\"chatId\": \"96170639378@c.us\",\r\n\t\"message\": \"I use Green-API to send this message to you!\"\r\n}"
# headers = {
# 'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data = payload)

# print(response.text.encode('utf8'))

from whatsapp_api_client_python import API
greenAPI = API.GreenAPI(
    "7103938518", "e33b3980940f40b5abd614cc34a6d867faf9136729524901ae"
)
response = greenAPI.sending.sendMessage("96170639378@c.us", "555")

print(response.data)