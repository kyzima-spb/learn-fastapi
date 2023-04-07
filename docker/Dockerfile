ARG PYVERSION=3.11
ARG RELEASE=slim-bullseye

FROM python:$PYVERSION-$RELEASE

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

STOPSIGNAL SIGINT

EXPOSE 5000

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONPATH "/python_packages:/project"
ENV USER_UID 1000
ENV USER_GID 1000
ENV FASTAPI_APP app:app
ENV FASTAPI_DEBUG 0

WORKDIR /app

RUN set -ex \
    && apt update \
    && apt install -yq --no-install-recommends \
        gettext-base \
        gosu \
    && pip install \
        --no-cache-dir \
        --disable-pip-version-check \
            fastapi \
            "uvicorn[standard]" \
            pythoninfo \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN set -ex \
   && groupadd -g 1000 user \
   && useradd -u 1000 -g user -s /bin/bash -m user

ARG USEFUL_URL="https://kyzima-spb.github.io/docker-useful/"
ADD $USEFUL_URL/switch-user/switch-user.sh /usr/local/bin/

RUN set -ex \
    && chmod 755 /usr/local/bin/*.sh

COPY ./root /

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["runserver"]
