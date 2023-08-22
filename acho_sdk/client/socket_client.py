import asyncio
import os
from typing import Optional
import socketio

class SocketClient:
    BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
    BASE_SOCKET_NAMESPACES = ['/soc']
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, token: Optional[str] = None, base_url = BASE_URL, socket_namespaces = BASE_SOCKET_NAMESPACES, sio = sio, timeout = 30):
        self.token = None if token is None else token.strip()
        """A JWT Token"""
        self.base_url = base_url
        self.socket_namespaces = socket_namespaces
        """A string representing the Acho API base URL.
        Default is `'https://kube.acho.io'`."""
        self.timeout = timeout
        """The maximum number of seconds client staying alive"""
        self.default_params = {}
        self.sio = sio


    async def conn(self, namespaces: Optional[list] = None):
        print(namespaces or self.socket_namespaces)
        try:
            await self.sio.connect(url=self.base_url, headers={ 'Authorization': '{} {}'.format('jwt', self.token) }, transports="polling")
        except Exception as e:
            print(e)
        

    @sio.on('connect', namespace='/soc')
    def on_connect():
        print("I'm connected to the /soc namespace!")
        return
    
    @sio.event
    async def connect():
        print('connected to server')
        return

    @sio.event
    async def disconnect():
        print('disconnected from server')
        return

    @sio.on('*', namespace='/soc')
    async def catch_all(event, data):
        print(event)
        print(data)
        return

    