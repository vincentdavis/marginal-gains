FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image.
COPY . .

# Install project dependencies.
RUN uv sync --frozen

# Run the app using the script.
CMD uv run streamlit run Marginal_Gains.py --server.address 0.0.0.0 --server.port $PORT --server.fileWatcherType none --browser.gatherUsageStats false --client.toolbarMode minimal
