import asyncio
from .http_client import HttpClient

class AppClient(HttpClient):

    def init(self, app_version_id: str):
        self.app_version_id = app_version_id
        return

    def push_event(self, event: dict):
        event.update({'scope': self.app_version_id})
        payload = {
            'scope': self.app_version_id,
            'event': event
        }
        response, text = asyncio.run(self.call_api(path="neurons/webhook", http_method="POST", json=payload))
        return (response, text)
    
    async def async_push_event(self, event: dict):
        event.update({'scope': self.app_version_id})
        payload = {
            'scope': self.app_version_id,
            'event': event
        }
        return await self.call_api(path="neurons/webhook", http_method="POST", json=payload)