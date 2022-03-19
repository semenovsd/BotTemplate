FROM python:3.8.6-alpine AS base
LABEL maintainer="semenov_sd@bk.ru"
ARG ENV_STAGE="production"
ARG UID=2000
ARG GID=2000
ARG TZ="Europe/Moscow"
ENV ENV_STAGE=$ENV_STAGE \
    UID=$UID \
    GID=$GID \
    TZ=$TZ \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION="1.1.4" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_HOME="/opt/poetry" \
    APP_DIR="/opt/app"
# Add Poetry and venv to PATH
ENV PATH="$POETRY_HOME/bin:$APP_DIR/.venv/bin:$PATH"
WORKDIR $APP_DIR


# 'Building' image
FROM base AS builder
ENV BUILD_DEPS="curl build-base postgresql-dev"
COPY poetry.lock pyproject.toml ./
RUN apk update \
    && apk add --no-cache $BUILD_DEPS \
    && python -m pip install --upgrade pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
    && poetry install $(test $ENV_STAGE == "production" && echo "--no-dev") --no-interaction --no-ansi \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_UNINSTALL=1 python \
    && echo $(scanelf --needed --nobanner --recursive ./.venv/ \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u) > run_deeps.txt \
    && apk del $BUILD_DEPS


# `Finally` image used for runtime
FROM base AS finally
LABEL stage=$ENV_STAGE
COPY --from=builder $APP_DIR $APP_DIR
RUN apk update \
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && cat run_deeps.txt | xargs apk add --no-cache \
    && apk add --no-cache shadow \
    && addgroup -g $GID user \
    && adduser -u $UID -D -G user user
COPY --chown=user:user . ./tgbot
USER user
ENTRYPOINT ["python", "-m", "tgbot"]
CMD ["--mode", "webhook"]