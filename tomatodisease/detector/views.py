from PIL import Image
import numpy as np
from io import BytesIO
from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response
import asyncio

from detector.utils import disease_detector

class TomatoDetector(APIView):
    async def post(self, request, *args, **kwargs):
        image = request.data.get('image')
        image_data = image.read()
        img = Image.open(BytesIO(image_data))
        
        result = await asyncio.gather(disease_detector(np.array(img)))

        res = {
            "result": result
        }
        print(result)

        return Response(res, status=status.HTTP_200_OK)

