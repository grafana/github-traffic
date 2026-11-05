FROM python:3.15-slim@sha256:8c13a3f37a6a5b71498228e902c4b9f51c1f7900d49fabf71f9a650c6120e0d0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY github-traffic.py /app/github-traffic.py

RUN useradd -u 1001 -m -s /sbin/nologin app
USER app

CMD [ "python3", "github-traffic.py"]
