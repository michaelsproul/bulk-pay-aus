FROM python:3.11

RUN pip3 install gunicorn

RUN mkdir /app
WORKDIR  /app
COPY . .

RUN pip3 install .

CMD exec gunicorn --bind 0.0.0.0:8000 bulk_pay:app
