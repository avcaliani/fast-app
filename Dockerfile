FROM python:3.10

# 👇 Environment Variables
ENV POETRY_VERSION='1.1.14' \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

WORKDIR /opt/app

# 👇 Installing Poetry
RUN apt-get update \
    && apt-get install -y build-essential python3-dev python3-setuptools curl \
    && pip install --upgrade --no-cache-dir pip \
    && curl -sSL https://install.python-poetry.org | python - --version "$POETRY_VERSION"

# 👇 Adding Files
COPY . .

# 👇 Installing project dependencies
RUN poetry install --no-dev

# 🤘 Let's rock
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "resources/log-config.yml"]
