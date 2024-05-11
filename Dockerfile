# Base Image
FROM python:3.12-slim

LABEL authors="vincentdavis"

ENTRYPOINT ["top", "-b"]


# Set working directory
WORKDIR ./

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN  pip install uv
RUN uv pip install -r requirements.txt

# Copy your Streamlit app code
COPY . .

# Expose Streamlit port (default: 8501)
EXPOSE 8501

# Start command (replace with your app's entry point if different)
CMD streamlit run Marginal_Gains.py --server.address 0.0.0.0 --server.port 8501 --server.fileWatcherType none --browser.gatherUsageStats false --client.toolbarMode minimal