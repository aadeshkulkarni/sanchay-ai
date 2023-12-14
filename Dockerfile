# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV INPUT_FILE_PATH="/app/videos/video.mp4"
ENV OPENAI_API_KEY=""
ENV OPENAI_MODEL="gpt-3.5-turbo-1106"
ENV MAX_TOKENS=15000
ENV OUTPUT_TYPE="vtt"
ENV OUTPUT_DIR="/app/output"

# Run run.sh when the container launches
CMD ["bash", "run.sh"]
