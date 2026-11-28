FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY github-traffic.py /app/github-traffic.py

RUN useradd -u 1001 -m -s /sbin/nologin app
USER app

CMD [ "python3", "github-traffic.py"]
