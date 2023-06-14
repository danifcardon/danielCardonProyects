# Dockerfile creation
FROM python:3.9
COPY . /app
WORKDIR /app

# Necessary dependencies created
RUN pip install tensorflow mysql-connector-python

# Execute the script
CMD [ "python", "image_classifier.py" ]

# Dockerfile image creation
docker build -t image-classifier .

# Execute the conteiner script
docker run image-classifier
