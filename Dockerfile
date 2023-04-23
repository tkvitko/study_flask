FROM python:3.9.1-buster

WORKDIR /blog

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY wsgi.py wsgi.py
COPY dev_config.json dev_config.json
COPY blog ./blog

EXPOSE 5000

CMD ["python", "wsgi.py"]
