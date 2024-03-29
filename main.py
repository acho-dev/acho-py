import asyncio
from acho.client.http_client import HttpClient


client = HttpClient(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjAyLCJmaXJzdG5hbWUiOiJUaW1vdGh5IiwibGFzdG5hbWUiOiJaaGFuZyIsImVtYWlsIjoiamlhbmhhb0BhY2hvLmlvIiwiY3VycmVudF90ZWFtX2lkIjoxNjUsImlhdCI6MTY2OTMxNDkyNywiZXhwIjoxNjY5OTE5NzI3fQ.MvOqDdz8rFbH1qdx8LzrPv0f0IO7DbUyDerrlhQDaH0", base_url="http://localhost:8888")

# response, meta = asyncio.run(client.call_api("health", "GET"))
# print(response.json())

response, meta = asyncio.run(client.call_api(path="neurons/webhook", http_method="POST", json={
  'scope': '549',
  'event': {
    'type': 'dataNode:onUpdate',
    'nodeId': 'ao8ZlBJkND-NrQ2dsrAMQ',
    'neuronId': 'f4736706-9c92-44af-a70f-5299130056cb',
    'scope': '549',
    'mount': 'data'
  }
}))
print(response.text)