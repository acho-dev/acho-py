import asyncio
import os
from typing import Optional

import socketio
from .http_client import HttpClient
from .socket_client import SocketClient

BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
BASE_SOCKET_NAMESPACES = ['/soc']
DEFAULT_SOCKET_NAMESPACE = '/soc'

class AppClient():
    
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, app_version_id: str, token: Optional[str] = None, base_url = BASE_URL, socket_namespaces = BASE_SOCKET_NAMESPACES, sio = sio, timeout = 30):
        self.socket = SocketClient(token=token, base_url=base_url, socket_namespaces=socket_namespaces, sio=sio, timeout=timeout)
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_version_id = app_version_id
        return

    def send_webhook(self, event: dict):
        event.update({'scope': self.app_version_id})
        payload = {
            'scope': self.app_version_id,
            'event': event
        }
        response, text = asyncio.run(self.http.call_api(path="neurons/webhook", http_method="POST", json=payload))
        return (response, text)
    
    async def async_send_webhook(self, event: dict):
        event.update({'scope': self.app_version_id})
        payload = {
            'scope': self.app_version_id,
            'event': event
        }
        return await self.http.call_api(path="neurons/webhook", http_method="POST", json=payload)
    
    def push_event(self, event: dict):
        event.update({'scope': self.app_version_id})
        asyncio.run(self.socket.sio.emit('push', event, namespace=DEFAULT_SOCKET_NAMESPACE))
        return