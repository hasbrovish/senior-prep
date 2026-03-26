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
# Interview prep content — markdown + binary files indexed by knowledge base
COPY Interview_Answers/*.md ./Interview_Answers/
# Interview Q&A sheets and prep programmes (XLSX + DOCX)
COPY trackers-docs/*.xlsx ./trackers-docs/
COPY trackers-docs/*.docx ./trackers-docs/
# Supplementary prep guides
COPY "02_Resumes/files/Supplementary_Prep_Guide_Complete.docx" ./02_Resumes/files/
COPY "02_Resumes/files/Top_1_Percent_Engineer_Preparation_Blueprint.docx" ./02_Resumes/files/
COPY 01_Career_Interview_Prep/THRIVING_PLAN_SDE2_SDE3.docx ./01_Career_Interview_Prep/
COPY 01_Career_Interview_Prep/INTERVIEW_MASTER_SHEET.docx ./01_Career_Interview_Prep/
COPY 01_Career_Interview_Prep/SDE2_Preparation_Analysis_January2026.docx ./01_Career_Interview_Prep/

# Create logs directory
RUN mkdir -p logs

# Non-root user for security
RUN useradd -m -u 1001 prepforge && chown -R prepforge:prepforge /app
USER prepforge

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
