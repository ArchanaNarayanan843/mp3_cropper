# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg

# Expose port 8501 for Streamlit
EXPOSE 8501

# Define environment variable
ENV NAME World

# Run Streamlit app
CMD ["streamlit", "run", "audio_cropper.py"]
