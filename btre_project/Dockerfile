FROM python:3.8-alpine

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev && apk add zlib-dev jpeg-dev gcc musl-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt /

RUN pip3 install --upgrade pip; \
    pip3 install -r /requirements.txt


COPY ./entrypoint.sh .
RUN chmod 777 ./entrypoint.sh

COPY . /app

WORKDIR /app


RUN mkdir -p /app/web/media
RUN mkdir -p /app/web/static
RUN adduser -D user
RUN chown -R user:user /app
RUN chmod -R 755 /app/web
USER user


ENTRYPOINT ["/entrypoint.sh"]