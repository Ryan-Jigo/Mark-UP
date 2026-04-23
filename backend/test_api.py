import requests
import json

url = "http://localhost:8000/extract/batch"
files = [
    ('files', ('varun.jpeg', open('c:/Users/ryanj/Mark-UP/backend/data/samples/varun.jpeg', 'rb'), 'image/jpeg')),
    ('files', ('abdu.jpeg', open('c:/Users/ryanj/Mark-UP/backend/data/samples/abdu.jpeg', 'rb'), 'image/jpeg')),
]
data = {
    'course': 'Test Course',
    'batch': 'Test Batch',
    'date': '2026-04-17',
    'exam': 'Test Exam'
}

response = requests.post(url, files=files, data=data)
with open('test_api_response.json', 'w') as f:
    json.dump(response.json(), f, indent=2)
