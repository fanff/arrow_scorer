# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV DEBIAN_FRONTEND=noninteractive

# Install uv (ultra-fast package manager)
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy only dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv
RUN uv pip install --system .

# Copy the entire project
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Set Streamlit config to run in headless mode (important for containers)
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false

# Run the Streamlit app
CMD ["streamlit", "run", "main.py"]
