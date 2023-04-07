#!/usr/bin/env bash

if [[ -z $USER_UID ]]; then
  USER_UID=$(id -u)
fi

if [[ -z $USER_GID ]]; then
  USER_GID=$(id -g)
fi

if [[ "$(id -u)" = '0' ]] && [[ "$USER_UID" != '0' ]]; then
  exec switch-user.sh -v \
    -d /app \
    -e "$BASH_SOURCE" \
      "$USER_UID:$USER_GID" "$*"
fi

if [[ "$1" = 'runserver' ]]; then
  args=("$FASTAPI_APP" '--host' '0.0.0.0' '--port' '5000')

  if [[ "$FASTAPI_DEBUG" != '0' ]]; then
    args+=('--reload')
    printf " * Mode:\tDevelopment\n"
  else
    printf " * Mode:\tProduction\n"
  fi

  exec uvicorn "${args[@]}"
fi

exec "$@"
