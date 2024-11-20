# Gunakan base image Python 3.11 slim
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Salin semua file dari lokal ke dalam container
COPY . /app/

# Install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Tentukan command untuk menjalankan aplikasi
CMD ["/opt/venv/bin/python", "app.py"]
