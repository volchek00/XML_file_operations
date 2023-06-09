# Use an official Python runtime as the base image
FROM python:3.11.3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY astra_export_xml.zip /app/
COPY app.py /app/
COPY templates/ /app/templates/

# Define the command to run your Flask app
CMD ["python", "app.py"]
