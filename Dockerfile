FROM python:3.10.9-slim

ENV POETRY_VERSION=1.4.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /opt

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]