FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /app/

RUN pip install --no-cache-dir .

RUN useradd --create-home --uid 3001 app
USER app

ENTRYPOINT [ "yamlvalidator" ]
CMD [ "--help" ]
