###########
# BUILDER #
###########

FROM python:3.9.6-alpine as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN pip install flake8==3.9.2
COPY ../../movies_admin/. .
RUN flake8 --ignore=E501,F401

COPY ../../requirements/requirements-movies_admin.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements-movies_admin.txt


#########
# FINAL #
#########

FROM python:3.9.6-alpine

RUN mkdir -p /home/app \
    && addgroup -S app && adduser -S app -G app

ENV HOME=/home/app \
    APP_HOME=/home/app/web \
    PYTHONPATH=$APP_HOME

RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements-movies_admin.txt .
RUN pip install --no-cache /wheels/*

COPY ../../docker/movies_admin/entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

COPY ../../movies_admin/. $APP_HOME

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
