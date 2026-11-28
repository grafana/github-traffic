FROM python:3.12-slim@sha256:5b5fe805d367f8f5a359ded6ab2652b7f9a206453ee6ee789c0045ba6ec15016

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY github-traffic.py /app/github-traffic.py

RUN useradd -u 1001 -m -s /sbin/nologin app
USER app

CMD [ "python3", "github-traffic.py"]
