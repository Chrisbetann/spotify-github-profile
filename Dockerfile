# Stage 1: Build stage
FROM python:3.11-bullseye AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./api/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim-bullseye

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY ./api /app

# Install Gunicorn for running the app
RUN pip install gunicorn

# Use Gunicorn to run the Flask app
CMD ["gunicorn", "-c", "gunicorn.conf.py", "view:app"]
