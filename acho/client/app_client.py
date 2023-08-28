import asyncio
import os
from typing import Optional

import socketio
from .http_client import HttpClient
from .socket_client import SocketClient

ACHO_TOKEN = os.environ.get("ACHO_PYTHON_SDK_TOKEN") or ""
BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
BASE_SOCKET_NAMESPACES = ['/soc']
DEFAULT_SOCKET_NAMESPACE = '/soc'
ACHO_CLIENT_TIMEOUT = 30
APP_ENDPOINTS = 'apps'

class App():
    
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, id: str, token: Optional[str] = ACHO_TOKEN, base_url = BASE_URL, timeout = ACHO_CLIENT_TIMEOUT):
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_id = id
        return

    def versions(self):
        response, text = asyncio.run(self.http.call_api(path=f"{APP_ENDPOINTS}/{self.id}/versions", http_method="GET"))
        return (response, text)
    
    def version(self, app_version_id: str):
        return AppVersion(app_version_id=app_version_id, token=self.http.token, base_url=self.http.base_url, timeout=self.http.timeout)
    
    def push_event(self, event: dict):
        print('Please specify version before publishing events')
        return
    
class AppVersion():
    
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, app_version_id: str, token: Optional[str] = None, base_url = BASE_URL, socket_namespaces = BASE_SOCKET_NAMESPACES, sio = sio, timeout = ACHO_CLIENT_TIMEOUT):
        self.socket = SocketClient(token=token, base_url=base_url, socket_namespaces=socket_namespaces, sio=sio, timeout=timeout)
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_version_id = app_version_id
        return
    
    def connect(self, namespaces: Optional[list] = None):
        try:
            self.socket.default_handlers()
            result = asyncio.run(self.socket.conn(namespaces=namespaces))
            return result
        except Exception as e:
            print(e)

    def join(self, namespaces: Optional[list] = None):
        print({'app_version_id': self.app_version_id, 'is_editing': True})
        result = asyncio.run(self.socket.emit('join_app_builder_room', {'app_version_id': self.app_version_id}, namespace=namespaces))
        return result

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