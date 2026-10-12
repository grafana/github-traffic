FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY github-traffic.py /app/github-traffic.py

RUN useradd -u 1001 -m -s /sbin/nologin app
USER app

CMD [ "python3", "github-traffic.py"]
