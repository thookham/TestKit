# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the scripts and profiles directories into the container
COPY scripts/ /app/scripts/
COPY profiles/ /app/profiles/

# Create a directory for exports (to be mounted as a volume)
RUN mkdir -p /app/exports

# Define the entrypoint to run the export script
ENTRYPOINT ["python", "scripts/export.py"]

# Default command (can be overridden)
CMD ["--help"]
