FROM python:3.8-alpine

COPY requirements.txt /requirements.txt

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
    && python -m venv --upgrade /aioweb \
    && /aioweb/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/aioweb/bin/pip install --no-cache-dir -r /requirements.txt" \
    && run_deps="$( \
            scanelf --needed --nobanner --recursive /aioweb \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $run_deps \
    && apk del .build-deps

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

ENV PATH="/usr/sbin:/usr/bin:/sbin:/bin:/aioweb/bin"

CMD python app.py
