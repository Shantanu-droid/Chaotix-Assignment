from django.urls import path
from .views import GenerateImageAPIView, ShowGeneratedImages

app_name = "core"

urlpatterns = [
    path('generate-images', GenerateImageAPIView.as_view(), name='generate_image'),
    path('show-images', ShowGeneratedImages.as_view(), name='generate_image'),
]

