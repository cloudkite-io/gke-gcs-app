FROM python:3.8-buster
WORKDIR /usr/app/
RUN apt-get update
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["/bin/bash", "-c", "python gcs.py"]
