from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery import group
from celery.result import AsyncResult
from .tasks import generate_sdxl_images
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor

class GenerateImageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        '''takes list of input texts and return list of submitted tasks'''
        data = request.data.get('text')
        if not data or not isinstance(data, list):
            return Response(
                'please provide valid list of texts',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        jobs = [generate_sdxl_images.delay(item) for item in data]
        return Response(
            {"task_ids":[job.id for job in jobs]}, 
            status=status.HTTP_202_ACCEPTED
        )
    
class ShowGeneratedImages(APIView):
    def get(self, request, *args, **kwargs):
        '''
        Simulate storing the resulting image URLs 
        or metadata in your Django model to demonstrate 
        how you might manage the image data.
        '''
        tasks = request.data.get('task_ids')
        if not tasks or not isinstance(tasks, list):
            return Response(
                'please provide valid list of task ids',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        urls = [AsyncResult(task) for task in tasks]
        url_states = [url.state for url in urls]
        if 'PENDING' in url_states:
            return Response(url_states, status=status.HTTP_200_OK)
        
        '''redering the images through html'''
        return render(
            request,
            'generators.html',
            {'images': [{"url": url.get(timeout=1)[0], "name": url.get(timeout=1)[0].split('.')[0]} for url in urls]}
        )
