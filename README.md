# Sanchay AI (A Generative AI app)

Upload your video and SanchayAI will generate key elements (video transcription, video subtitles, and video chapters) in an organized and easily accessible manner.

### Project Status and Contribution Potential

This project is in its infancy and has just been scaffolded with a new architecture. It's at a crucial stage where contributions can significantly shape its future and scalability. With the right environment and collaborative effort, it has the potential to evolve into something truly remarkable.

### System (In a nutshell)
![System](/docs/system.png)


### Requirements:
- MongoDB
- RabbitMQ
- Localstack


There are 2 apps:

1. web-app
- This is a fullstack NextJS app. 
- The project depends on 3 services:
    - RabbitMQ
    - Localstack
    - MongoDB

2. worker
- This is a Python based RabbitMQ worker that listens to request from web-app and processes them in the background.
- The project also depends on 3 services:
    - RabbitMQ
    - Localstack
    - MongoDB


### Setup

Before setting up the codebase, it's important to setup the services the codebase depends on.

### Setup RabbitMQ locally
- If you have docker installed on your system, you can setup RabbitMQ using the command
    - `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management`
    - This will spinup RabbitMQ on localhost:15672 (default username/password = guest/guest)
> OR

- If you don't want to setup using docker, you can setup RabbitMQ by following steps [here](https://www.rabbitmq.com/docs/download)

### Setup MongoDB
- Recommended: Create a database cluster on https://cloud.mongodb.com/ for free and use the connection string

### Localstack
- Follow the guide mentioned here- https://app.localstack.cloud/getting-started
- Create a new bucket by running the command `aws s3 mb s3://sanchayai --endpoint-url=http://localhost:4566`

Once the above services are up, clone the sanchay-ai repository

### Worker setup
- cd into apps/worker folder
- follow readme instructions
- pip install
- python consumer.py

### Web-app setup
- cd into apps/web-app folder
- follow readme instructions
- npm install
- npm run dev

If all is working well,
- Your Web-app should be listening on `localhost:3000`
- Your Rabbit-MQ should be working on `http://localhost:15672/`
- Your localstack should be working on `http://localhost:4566` (nothing to display on chrome here)


You can run the app and upload a test video which is available in the codebase here - ./docs/video.mp4

![Home](/docs/app-1.png)
![Videos](/docs/app-2.png)
