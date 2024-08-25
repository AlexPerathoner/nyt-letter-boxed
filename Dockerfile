# Use the official Python image from the Docker Hub
FROM python:3.12.4-slim

# also install nohup
# use apk instead of apt-get (not available in alpine) - nohup is part of coreutils
# https://stackoverflow.com/a/56212487/6884062 apk is in /sbin - /sbin is empty. going back to -slim
RUN apt-get update && apt-get install -y coreutils

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for logs
RUN mkdir -p /app/logs

# no ports exposed. Defined in docker-compose.yml

# Command to run the Flask application, nohup redirects output to nohup.out
CMD nohup flask run --host=0.0.0.0 > /app/logs/flask.log 2>&1
# nohup flask run --host=0.0.0.0 --cert=cert.pem --key=key.pem &

# Define a volume for logs
VOLUME ["/app/logs"]