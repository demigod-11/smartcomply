FROM python:3.12-slim-bookworm AS rust-builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    patchelf \
    && rm -rf /var/lib/apt/lists/* \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain 1.77.0
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --no-cache-dir maturin

WORKDIR /build
COPY rust/tm_rules/Cargo.toml rust/tm_rules/pyproject.toml rust/tm_rules/
COPY rust/tm_rules/src rust/tm_rules/src
RUN cd rust/tm_rules && maturin build --release

FROM python:3.12-slim-bookworm AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-ansi

COPY --from=rust-builder /build/rust/tm_rules/target/wheels/*.whl /tmp/wheels/
RUN pip install --no-cache-dir /tmp/wheels/*.whl || true

COPY src/ ./src/
WORKDIR /app/src

EXPOSE 8000

FROM runtime AS test
WORKDIR /app
COPY tests/ ./tests/
RUN poetry install --no-ansi
ENV DJANGO_ENV=test
CMD ["pytest", "tests", "-v", "--tb=short"]
