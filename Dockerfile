# Pull base image
FROM python:3.6-slim

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
ADD . /code/

