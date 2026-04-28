FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYLSL_LIB=/app/liblsl-1.17.7-jammy_amd64/lib/liblsl.so.1.17.7

WORKDIR /app

RUN pip install --upgrade pip uv

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

COPY . .

RUN python -c "import app, flask, flask_cors, flask_socketio; print('Container web dependency smoke check passed')"

EXPOSE 5000

CMD ["python", "app.py"]
