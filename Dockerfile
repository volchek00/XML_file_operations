# Use an official Python runtime as the base image
FROM python:3.11.3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the XML file and Python script to the container
COPY astra_export_xml.zip /app/
COPY final_file.py /app/

# Define the command to run your Python script
CMD ["python", "final_file.py"]
