# Public World Builder generate/run backend for the personal netcup VPS.
#
# Build context (assembled by personal-vps `apps/world-builder/deploy.sh`):
#   app/         this repository at the deployed commit (git archive)
#   llm_client/  BrianMills2718/llm_client at the pinned revision, .git included
#
# The service needs only the standard library plus llm_client. It binds inside the
# container; the edge tunnel reaches it by container name, and the brianmills.dev Worker
# proxies /world-builder/api/* to it. All mutable state (the persistent daily LLM spend
# ledger under $HOME/.local/state/world-builder and llm_client observability) lives in /data.
FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin app

COPY llm_client /opt/llm_client
RUN pip install --no-cache-dir -e /opt/llm_client \
    && git config --system --add safe.directory /opt/llm_client

COPY app /opt/app
WORKDIR /opt/app
RUN install -d -o app -g app /data

ARG BUILD_COMMIT=unknown
ARG LLM_CLIENT_REVISION
RUN test -n "${LLM_CLIENT_REVISION}" \
    && test "$(git -C /opt/llm_client rev-parse HEAD)" = "${LLM_CLIENT_REVISION}"
ENV WORLD_SUBSTRATE_BUILD_COMMIT=${BUILD_COMMIT} \
    LLM_CLIENT_REVISION=${LLM_CLIENT_REVISION} \
    LLM_CLIENT_DATA_ROOT=/data/llm_client/logs \
    LLM_CLIENT_DB_PATH=/data/llm_client/llm_observability.db \
    LLM_CLIENT_PROJECT=world-substrate \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/data/home

USER app
EXPOSE 8813
HEALTHCHECK --interval=60s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8813/world-builder/api/health', timeout=8)"
CMD ["python", "scripts/world_builder_service.py", "--host", "0.0.0.0", "--port", "8813"]
