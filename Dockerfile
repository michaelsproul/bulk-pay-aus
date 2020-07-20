FROM python:3.5

RUN pip3 install pip==18 \
    && pip3 install gunicorn

RUN mkdir /app
WORKDIR  /app
COPY . .

RUN pip3 install --upgrade --process-dependency-links .

CMD gunicorn --bind 0.0.0.0:8000 bulk_pay:app
