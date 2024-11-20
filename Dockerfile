FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

ENV FLASK_RUN_HOST=0.0.0.0



CMD ["/opt/venv/bin/python", "app.py"]
