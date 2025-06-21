FROM python:3.12-slim

# Set the path to the virtual environment.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Set the working directory.
WORKDIR /app

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /uvx /bin/

# Copy only requirements files for dependency installation
COPY uv.lock pyproject.toml ./

# Install dependencies using uv sync as specified
RUN uv sync --frozen --no-cache

# Add virtual environment's bin directory to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of the application code AFTER dependencies are installed
COPY . .

# Run the application.
CMD ["uvicorn", "app.main:app", "--port", "5000", "--host", "0.0.0.0"]
