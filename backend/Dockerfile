FROM python:3.10-alpine as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH "${PYTHONPATH}:/"

RUN apk update && apk add curl python3-dev g++ libc-dev libffi-dev libpq-dev \
    && curl 'https://bootstrap.pypa.io/get-pip.py' -o get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py && pip install poetry

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY poetry.lock pyproject.toml /
RUN --mount=type=cache,target=/root/.cache poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt && pip install --force-reinstall -r requirements.txt


FROM python:3.10-alpine
COPY --from=builder /opt/venv /opt/venv
COPY application/ application/
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PATH="/opt/venv/bin:$PATH"
CMD uvicorn application.app:app --host 0.0.0.0 --reload
