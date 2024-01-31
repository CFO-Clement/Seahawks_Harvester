FROM python:3.11-slim
ARG NESTER_PORT
WORKDIR .

RUN apt-get update && apt-get install -y \
    python3-tk \
    nmap \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.env config.env

COPY /src /src
EXPOSE $NESTER_PORT

CMD ["python", "./src/app.py"]