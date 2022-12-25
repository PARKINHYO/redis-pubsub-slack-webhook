FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
CMD [ "python3", "main.py"]