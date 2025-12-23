FROM python:3.11-slim


# 🔧 Dépendances système nécessaires à LightGBM
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "8000"]
