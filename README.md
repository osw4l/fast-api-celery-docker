# Welcome to Fast Api Celery with Flower On Docker

little project to start with fast api, celery, flower, periodic tasks and redis

# Containers

 - **Backend** (It runs fast api)
 - **Redis** (As Broker)
 - **Worker** (It runs the background jobs)
 - **Beat** (Send periodic jobs to the worker)
 - **Flower** (Tasks monitor)
 - **FTP** (FTP server running on pure-ftpd)
 - **Prometheus** (Service to collect and view data)
 - **Grafana** (Dashboard to see data)

# Links to open into browser

 - **Backend** (http://localhost:4000/docs)
 - **Flower** (http://localhost:5000/tasks)
 - **Grafana** (http://localhost:3000)
 - **Prometheus** (http://localhost:9090)

## How to run

**Create .env file**

    cp env_template .env
  
  **Build the image**

    docker-compose build
  
   **Up the image**

    docker-compose up

   **Up the image permanently**

    docker-compose up -d

## How to stop and get down

   **To stop the image**
  
      docker-compose stop

   **To get down**
  
      docker-compose down

## 💚 Made with love by osw4l 💚

