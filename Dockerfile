FROM tiangolo/uvicorn-gunicorn-fastapi

COPY ./requirements.txt /app

COPY ./app /app/app

RUN pip install -r requirements.txt
