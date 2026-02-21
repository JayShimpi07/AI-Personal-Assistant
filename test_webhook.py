import requests
user_message = "What is Quantum Physics in 3-4 lines?"
request_message = {'message': user_message}
url = "https://jayshimpi07.app.n8n.cloud/webhook-test/6e55ccdc-3ac9-43e1-9900-eefca464488e"
response = requests.post(url, json=request_message)
print(response.status_code)
print(response.json()[0]["output"])