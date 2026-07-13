FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser

# Copy requirements and install dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY --chown=appuser:appuser . .

# Ensure data directory exists (recommended to mount as a volume)
RUN mkdir -p data

EXPOSE 8000

# Run Uvicorn
CMD ["uvicorn", "Backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
