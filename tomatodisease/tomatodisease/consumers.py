import base64
from channels.generic.websocket import AsyncWebsocketConsumer
import websockets
from PIL import Image
from io import BytesIO
import asyncio
from django.http import HttpResponse

async def receive_image(websocket):
    while True:
        try:
            image_data = await websocket.recv();
            image = Image.open(BytesIO(image_data))
            image.save("1.jpg")
            await asyncio.sleep(0) # cho phep cac tac vu bat dong bo khac chay neu co
        except websockets.exceptions.ConnectionClosedOK:
            pass

async def lobby():
    async with websockets.connect('ws://192.168.1.27:60') as websocket:
        receive_task = asyncio.create_task(receive_image(websocket))
    
# def lobby_sync(request):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(lobby())

#     with open("1.jpg", "rb") as f:
#         image_data = f.read()
#     return HttpResponse(image_data, content_type="image/jpeg")


class ImageConsumer(AsyncWebsocketConsumer):
    def __init__(self, app):
        self.app = app

    async def connect(self):
        await self.accept()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(lobby())
        with open("1.jpg", "rb") as f:
            image_data = f.read()
        self.send(image_data)
            

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Xử lý dữ liệu hình ảnh ở đây
        image_data = base64.b64decode(text_data)
        # Gửi dữ liệu hình ảnh tới client
        await self.send(image_data)