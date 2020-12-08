FROM python:3.8-buster
WORKDIR /usr/app/
RUN apt-get update
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip install gunicorn
COPY . .
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:5000 --workers 2  run:app"]
