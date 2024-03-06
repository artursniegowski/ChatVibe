FROM python:3.12-alpine3.19
LABEL maintainer="artursniegowski"

ENV PYTHONDONTWRITEBYTECODE 1 

ENV PYTHONUNBUFFERED 1

COPY ./requirements /temp/requirements/
COPY ./app /app

WORKDIR /app

EXPOSE 8000

# adding dep to run psycopg: postgresql-libs postgresql-dev gcc musl-dev
RUN apk add --update --no-cache postgresql-libs postgresql-dev musl-dev && \
    apk add --update --no-cache --virtual .temp-build-deps \
        gcc && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /temp/requirements/dev.txt && \
    # cleaning
    rm -rf /temp && \
    # Remove the temporary build dependencies
    apk del .temp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # storage for static files - STATIC_ROOT and MEDIA_ROOT
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user