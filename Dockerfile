FROM python:3.8-slim

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN apt-get clean \
  && apt-get -y update \
  && apt-get -y install python3-dev \
  && apt-get -y install build-essential \
  && pip install pip --upgrade \
  && pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . /code

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "apps.api.entrypoint:app"]