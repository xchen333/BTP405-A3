FROM python:3.8

WORKDIR /app

RUN apt update && apt install -y netcat-openbsd

COPY main.py /app/
COPY init.sql /app/
COPY wait-for-it.sh /app/

RUN pip install mysql-connector-python

RUN chmod +x /app/wait-for-it.sh

EXPOSE 8000

CMD ["sh", "-c", "/app/wait-for-it.sh db 3306 -- python main.py"]
