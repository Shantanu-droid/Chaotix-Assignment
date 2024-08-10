# Chaotix-Assignment
Develop a Django application that generates 3 images in parallel using Stabilit AI’s Text-to-image generation API.  Use Celery for parallel processing to manage asynchronous calls to the API.

# Django Project with Celery and Redis Integration

## Overview

This project is a Django application configured to handle API requests and manage asynchronous tasks using Celery and Redis. The application includes functionality for generating images based on text input, storing the images, and rendering them with Django templates.

## Prerequisites

- Python 3.12 or above
- Docker and Docker Compose
- Redis (if not using Docker)

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

