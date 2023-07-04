[![Build Status](https://app.travis-ci.com/Fhockk/SPA-Comments.svg?token=EEVwf1MVsF8FEmpkxpRC&branch=master)](https://app.travis-ci.com/Fhockk/SPA-Comments)

## About
- It is a test project.

- The purpose of the project is to demonstrate my skills and knowledge of the back-end development processes.

## Technical Requirements
- Use PEP8 for your Python code
- Python 3
- Django, Django ORM
- JWT
- PostgreSQL
- Redis
- Docker

# Installation:

## Clone the repo

```shell
git clone https://github.com/Fhockk/SPA-Comments.git
```

## How to run this project?
- Make sure you have docker installed
- Open the terminal and hit the following command :

Change the directory:
```shell
cd SPA-Comments/
```

## Create the .env file like .env.example with ur value to:

- SECRET_KEY=(your value)
- DEBUG=(your value)

## Run the docker build (development server)
```shell
docker-compose up --build
```

- API will be available at the addresses: http://127.0.0.1:8000/api/comments/, http://127.0.0.1:8000/api/users/
- Detailed specifications you can find http://127.0.0.1:8000/api/swagger/.
