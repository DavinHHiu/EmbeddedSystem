import asyncio
import websockets
import binascii
from io import BytesIO
import base64
import numpy as np
import cv2
import socket
# socket.getaddrinfo('http://192.168.1.27', 3001)

from PIL import Image, UnidentifiedImageError

def is_valid_image(image_bytes):
    try:
        Image.open(BytesIO(image_bytes))
        # print("image OK")
        return True
    except UnidentifiedImageError:
        print("image invalid")
        return False
    
async def receive_images():
    async with websockets.connect('ws://192.168.1.27:60') as websocket:
        while True:
            image_data = await websocket.recv()
            image = Image.open(BytesIO(image_data))
            image.save("1.jpg")

            img = cv2.imread("1.jpg", cv2.IMREAD_COLOR)
            
            cv2.imshow('Received Image', img)
            cv2.waitKey(1)

asyncio.get_event_loop().run_until_complete(receive_images())
