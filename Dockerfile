# syntax=docker/dockerfile:1

FROM python:3.8.3-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 443

CMD [ "python", "-m" , "app"]
# CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--cert=adhoc"]