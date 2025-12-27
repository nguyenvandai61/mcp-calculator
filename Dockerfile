# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port if using SSE (default MCP port is often 8000, but stdio doesn't use a port)
EXPOSE 8000

# Set environment variable for MCP endpoint
ENV MCP_ENDPOINT=""

# Run the application using the pipe
CMD ["python", "mcp_pipe.py", "app.py"]
