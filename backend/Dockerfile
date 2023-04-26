FROM kyzimaspb/fastapi:3.11-slim-bullseye

COPY ./requirements.txt ./

RUN set -ex \
    && pip install \
        --no-cache-dir \
        --disable-pip-version-check \
        -r requirements.txt

COPY . ./
