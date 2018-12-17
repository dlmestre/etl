FROM python:3.6

COPY ./application/requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./application/app /app
WORKDIR /app

ENTRYPOINT ["python", "app.py"]
