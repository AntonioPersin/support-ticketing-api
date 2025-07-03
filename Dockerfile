# Dockerfile
FROM python:3.11-slim

# Radni direktorij unutar kontejnera
WORKDIR /app

# Kopiraj ovisnosti i instaliraj ih
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj ostatak aplikacije
COPY . .

# Expose porta
EXPOSE 8000

# Pokreni aplikaciju
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
