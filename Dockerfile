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
# War plan docs and reference files
COPY docs/ ./docs/
# Interview prep content (Interview_Answers/) — indexed by knowledge base for AI coach
# Only copy .md and .txt files (skip PDFs/DOCX/XLSX to keep image size small)
COPY Interview_Answers/*.md ./Interview_Answers/

# Create logs directory
RUN mkdir -p logs

# Non-root user for security
RUN useradd -m -u 1001 prepforge && chown -R prepforge:prepforge /app
USER prepforge

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
