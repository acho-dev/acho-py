import asyncio
from acho_sdk.client.http_client import HttpClient


client = HttpClient(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjAyLCJmaXJzdG5hbWUiOiJUaW1vdGh5IiwibGFzdG5hbWUiOiJaaGFuZyIsImVtYWlsIjoiamlhbmhhb0BhY2hvLmlvIiwiY3VycmVudF90ZWFtX2lkIjoxNjUsImlhdCI6MTY2OTMxNDkyNywiZXhwIjoxNjY5OTE5NzI3fQ.MvOqDdz8rFbH1qdx8LzrPv0f0IO7DbUyDerrlhQDaH0", base_url="http://localhost:8888")
result = asyncio.run(client.call_api("health", "GET"))

print(result)