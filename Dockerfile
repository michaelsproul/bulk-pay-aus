# Transpile JS in a separate builder container.
FROM node:21 AS js_builder
WORKDIR /app
COPY . /app
RUN ["yarn", "add", "webpack", "webpack-cli"]
RUN ["yarn", "build"]

# Run backend in a Python container with compiled JS copied from builder.
FROM python:3.11
RUN pip3 install gunicorn
RUN mkdir /app
WORKDIR  /app
COPY . .
RUN pip3 install .
COPY --from=js_builder /app/bulk_pay/static/bulk_pay.bundle.js /app/bulk_pay/static/bulk_pay.bundle.js

CMD exec gunicorn --bind 0.0.0.0:8000 bulk_pay:app
