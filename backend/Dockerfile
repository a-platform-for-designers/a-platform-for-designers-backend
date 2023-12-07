FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x wait-for-it.sh entrypoint.sh entrypoint_daphne.sh

ENTRYPOINT ["/app/entrypoint.sh"]
