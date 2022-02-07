# syntax=docker/dockerfile:1

FROM python:3.8.2-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]