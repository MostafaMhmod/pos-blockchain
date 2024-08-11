# pull official base image
FROM bitnami/python:3.11.5

# set working directory
WORKDIR /usr/src/node

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get clean

# copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy all files
COPY . .

# make entrypoint script executable
RUN chmod +x entrypoint.sh