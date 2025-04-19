import os
import sys

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ImageUploadSerializer
from scripts.test_cnn import predict_image

# Create your views here.


class ImageUploadView(APIView):
    def post(self, req, *arg, **kwargs):
        serializer = ImageUploadSerializer(data=req.data)
        print('req.data', req.data)
        if serializer.is_valid():
            instance = serializer.save()
            print('instance', instance)
            # Get the image path
            image_path = instance.image.path
            print('image_path', image_path)

            predicted_class, confidence = predict_image(image_path)

            response_data = {}
            response_data['prediction'] = predicted_class
            response_data['confidence'] = confidence

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)