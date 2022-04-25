# pull official base image
FROM python:3.9.10-alpine3.15

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code

# copy project
COPY . /code/

# install psycopg2 dependencies
RUN apk update \
    && apk upgrade \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev openssl-dev libffi-dev jpeg-dev zlib-dev freetype freetype-dev \
    && apk add cairo-dev pango-dev gdk-pixbuf fontconfig ttf-freefont font-noto terminus-font \
    && pip3 install --upgrade pip

# Install dependencies
RUN pip install pipenv && pipenv install --system

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

