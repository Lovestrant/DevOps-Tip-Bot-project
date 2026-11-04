FROM python:3.12-slim

WORKDIR /app
COPY app.py .

# Overridden at build time by Jenkins
ARG BUILD_TAG=local
ENV BUILD_TAG=${BUILD_TAG}

CMD ["python", "app.py"]
