import requests

url = "https://oauth2.googleapis.com/token"
data = {
    "client_id": "716682036624-mferj6k8surnn317tvg9pc3ae65temu3.apps.googleusercontent.com",
    "client_secret": "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",
    "refresh_token": "1//0hj1vy0qsTeaSCgYIARAAGBESNwF-L9IrAKi3iTWNP5UgGMDHnHEVu0BFHhvKvbR92n-0vg9EzBJfSQPX42pGxWHnNkRftKmBOIU",
    "grant_type": "refresh_token"
}

response = requests.post(url, data=data)

print(response.json())
