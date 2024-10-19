# Specifica la versione di Python
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Ambiente Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/opt/poetry' \
    POETRY_VERSION=1.8.4

WORKDIR /home/

# Definisce l'utente
ARG APP_USER=appuser
ENV APP_USER=${APP_USER}
ARG APP_UID=1000
ARG APP_GID=1000

# Creazione gruppo e utente
RUN groupadd -g ${APP_GID} ${APP_USER} && \
    useradd -u ${APP_UID} -g ${APP_GID} -M -s /usr/sbin/nologin ${APP_USER}

# Installa dipendenze di sistema e build tools
RUN apt-get update && apt-get install -y gosu dos2unix build-essential curl

# Installa Poetry senza collegamento simbolico
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    $POETRY_HOME/bin/poetry config virtualenvs.create false

# Aggiungi Poetry al PATH
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Copia solo i file di Poetry per caching
COPY poetry.lock pyproject.toml /home/

# Configura l'ambiente e installa i pacchetti usando Poetry
RUN poetry install --only=main --no-dev --no-root --no-interaction --no-ansi

# Imposta il PYTHONPATH
ENV PYTHONPATH=/home

# Copia l'applicazione
COPY ./app /home/app
COPY ./scripts /home/scripts

# Conversione dei file script a formato Unix e settaggio dei permessi
RUN dos2unix /home/scripts/init.sh && \
    chmod +x /home/scripts/init.sh && \
    chown -R ${APP_USER}:${APP_USER} /home

# Esposizione della porta
EXPOSE 5000

# Entrypoint
ENTRYPOINT [ "/bin/bash", "/home/scripts/init.sh" ]
