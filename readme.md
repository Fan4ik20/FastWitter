# FastWitter
## Description
An API for a social network in which you can share text posts,  
follow other users, like and comment their publication
## Requirements
- Python 3.10
### Or
- Docker
## Installation
- clone this repo via command  
  - `git clone https://github.com/Fan4ik20/FastWitter.git`
## After Installation
- If you want to run an application using python
  - install the requirements  
    - `cd fastwitter && pip install -r requirements.txt`
- Specify .env file in fast_witter directory  
  with there variables in the format `variable=value`
  - DB_URL
  - SECRET_KEY
## Running 
- ### Directly via Python
  - You must be in the fast_witter directory
  - You can run application via command  
    - `uvicorn main:app --reload`
- ### Docker
  - Build images via command  
    - `docker compose build`
  - Run containers via command
    - `docker compose up -d`
  - To stop the containers use
    - `docker compose stop`
  - To stop and remove containers use
    - `docker compose down`
## Links
https://github.com/Fan4ik20/fastwitter