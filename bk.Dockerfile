# Base Image
FROM python:3.12-slim

LABEL authors="vincentdavis"

ENTRYPOINT ["top", "-b"]


# Set working directory
# WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY . .
RUN pip install --no-cache -r requirements.txt

# Expose Streamlit port (default: 8501)
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health


ENTRYPOINT ["streamlit", "run", "Marginal_Gains.py", "--server.port=8501", "--server.address=0.0.0.0"]