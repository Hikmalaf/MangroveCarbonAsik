# Gunakan image dasar Python
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file aplikasi ke dalam container
COPY . /app/

# Install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Set environment variable untuk menghindari masalah dengan Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0  # Agar Flask dapat diakses dari luar container

# Tentukan perintah untuk menjalankan aplikasi
CMD ["/opt/venv/bin/python", "app.py"]
