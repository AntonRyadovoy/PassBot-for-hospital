FROM python:3.11-slim

WORKDIR /opt/DMK_bot

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "Pass.py"] 