# Chaotix-Assignment
Develop a Django application that generates 3 images in parallel using Stabilit AI’s Text-to-image generation API.  Use Celery for parallel processing to manage asynchronous calls to the API.

# Django Project with Celery and Redis Integration

## Overview

This project is a Django application configured to handle API requests and manage asynchronous tasks using Celery and Redis. The application includes functionality for generating images based on text input, storing the images, and rendering them with Django templates.

## Prerequisites

- Python 3.12 or above
- Docker and Docker Compose
- Redis (if not using Docker)

## Celery configuration files
![image](https://github.com/user-attachments/assets/b8839c66-49b5-423b-b1f0-129ac590581e)
```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chotix.settings')
app = Celery('chotix')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

![image](https://github.com/user-attachments/assets/d513de86-51b2-47e7-ac25-36324ce9572c)

```bash
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

![image](https://github.com/user-attachments/assets/a7fe2a21-8c9c-44fd-9853-c72265d55459)
```yaml
version: '3.8'

services:
  django:
    build: .
    container_name: django
    command: python3 manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - redis
    env_file:
      - .env
    environment:
      - SDLX_API_KEY=<your key>
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A chotix worker -l INFO
    volumes:
      - .:/app
    depends_on:
      - django
      - redis
    env_file:
      - .env
    environment:
      - DEBUG=1
      - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
```
## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Shantanu-droid/Chaotix-Assignment.git
cd yourproject
```

### Running with Docker
The application is set up to run within Docker containers, including Django, Celery workers, and Redis.

### Build and Run Containers
```bash
cd chotix
docker-compose up --build
```
### Using the Application
### Generating Images: 
Submit a list of text inputs for your images...

``` curl
curl --location 'localhost:8000/generate-images' \
--header 'Content-Type: application/json' \
--data '{
    "text":["A red flying dog","A piano ninja", "A footballer kid"]
}'
```
You will get a list of task ids...

```json
{
    "task_ids": [
        "06b9e3ef-a8f8-42aa-bb5a-d71fa144959e",
        "b104bdb4-4003-4bd1-acfd-1b575f54d8fe",
        "457ce114-6817-4a19-beed-a75e2329ef2e"
    ]
}
```


### Viewing Images:
Once generated, images can be viewed in the web interface, where each image will be displayed with its name as a footer.

``` curl
curl --location --request GET 'localhost:8000/show-images' \
--header 'Content-Type: application/json' \
--data '{
    "task_ids": [
        "06b9e3ef-a8f8-42aa-bb5a-d71fa144959e",
        "b104bdb4-4003-4bd1-acfd-1b575f54d8fe",
        "457ce114-6817-4a19-beed-a75e2329ef2e"
    ]
}'
```
##### note: replace task_ids with the results from generate image api
If you are using a api manager(like postman) you can see the requested images
![image](https://github.com/user-attachments/assets/42c5a905-4420-4ab0-b112-e0222d4f71df)
![image](https://github.com/user-attachments/assets/0967ff41-be51-43f3-940a-ec6bb3b03b00)

![image](https://github.com/user-attachments/assets/7bf902e7-16aa-41b6-b3f9-24950da1e7b3)
![image](https://github.com/user-attachments/assets/a5411a7a-efe5-4cbf-90bd-1baf2b209a7b)

