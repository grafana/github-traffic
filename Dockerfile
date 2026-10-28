FROM python:3.12-slim@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY github-traffic.py /app/github-traffic.py

RUN useradd -u 1001 -m -s /sbin/nologin app
USER app

CMD [ "python3", "github-traffic.py"]
