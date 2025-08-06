# Use the official Node.js 20 image as a base
FROM node:20-slim

# Set the working directory inside the container
WORKDIR /app/frontend

# Copy package.json and package-lock.json to the container
# This optimizes Docker's caching
COPY package*.json ./

# Install the project dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# The command to run when the container starts
CMD ["npm", "run", "dev", "--", "--host"]
