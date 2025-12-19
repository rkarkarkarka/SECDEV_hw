# syntax=docker/dockerfile:1.7-labs
ARG PYTHON_VERSION=3.11.9

FROM python:${PYTHON_VERSION}-slim AS build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --wheel-dir=/tmp/wheels -r requirements.txt
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY . .
RUN pytest -q

FROM python:${PYTHON_VERSION}-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd --system app && useradd --system --gid app app
COPY --from=build /tmp/wheels /tmp/wheels
RUN pip install --no-cache-dir /tmp/wheels/* && rm -rf /tmp/wheels
COPY --from=build /app/app ./app
COPY --from=build /app/src ./src
COPY --from=build /app/pyproject.toml ./pyproject.toml
COPY --from=build /app/README.md ./README.md
COPY --from=build /app/uploads ./uploads
RUN chown -R app:app /app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
