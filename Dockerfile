FROM python:3.11-alpine

WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

