# ─── Stage 1: Build React UI ─────────────────────────────────────────────────
FROM node:22-slim AS ui-build
WORKDIR /workspace
COPY ui/ ./ui/
RUN cd ui && npm ci && npm run build
# Vite outputs to /workspace/portal/ (../portal relative to ui/)

# ─── Stage 2: Python application ─────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY intel/ ./intel/
COPY prep.py .
# Curriculum JSONs needed by /api/curriculum
COPY data/*.json ./data/
# War plan docs, reference files + Alex Xu PDFs (knowledge base)
COPY docs/ ./docs/
# Interview prep content — markdown + HTML files indexed by knowledge base
COPY Interview_Answers/*.md ./Interview_Answers/
COPY Interview_Answers/*.html ./Interview_Answers/

# Copy built React UI from stage 1
COPY --from=ui-build /workspace/portal/ ./portal/

# Create logs directory
RUN mkdir -p logs

# Non-root user for security
RUN useradd -m -u 1001 prepforge && chown -R prepforge:prepforge /app
USER prepforge

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
