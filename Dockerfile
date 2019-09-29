FROM python:3.6-alpine

RUN adduser -D instagram
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache build-base jpeg-dev zlib-dev

WORKDIR /home/instagram

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install psycopg2-binary
RUN venv/bin/pip install --no-cache-dir pillow
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY instagram.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP instagram.py

RUN chown -R instagram:instagram ./
USER instagram

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]