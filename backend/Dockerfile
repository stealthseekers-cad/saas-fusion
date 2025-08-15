# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# --- SECURITY HARDENING ---
# Upgrade core packaging tools to the latest versions to mitigate known vulnerabilities
# before installing any other dependencies.
RUN pip install --upgrade pip setuptools wheel

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
