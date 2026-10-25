FROM python:3.12-slim

WORKDIR /app

ARG APP_VERSION=0.0.0
ARG GIT_COMMIT=unknown
ARG GIT_REPO=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.source="${GIT_REPO}" \
      org.opencontainers.image.created="${BUILD_DATE}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py VERSION ./

EXPOSE 5000

CMD ["python", "app.py"]
