FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY intel/ ./intel/
COPY portal/ ./portal/
COPY prep.py .
# Curriculum JSONs needed by /api/curriculum
COPY data/*.json ./data/
# War plan docs, reference files + Alex Xu PDFs (knowledge base)
COPY docs/ ./docs/
# Note: Interview_Answers/ is in .gitignore (local only) — KB auto-discovers at runtime
# Note: trackers-docs/ is in .gitignore (local only) — not needed in container

# Create logs directory
RUN mkdir -p logs

# Non-root user for security
RUN useradd -m -u 1001 prepforge && chown -R prepforge:prepforge /app
USER prepforge

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
