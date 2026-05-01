FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



# WHAT THIS DOES:-

# uses Python 3.11
# sets /app as working directory
# Installs dependencies
# copies your code
# starts FastAPI with Uvicorn