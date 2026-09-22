# Canonical task base. Harness Smoke's runtime binder changes only this default
# to a preinstalled agent image; all repository preparation remains below.
ARG HARNESS_SMOKE_BASE_IMAGE=python:3.12-slim
FROM ${HARNESS_SMOKE_BASE_IMAGE}

WORKDIR /app
COPY repo/ /app/
COPY setup/ /tmp/harness-smoke-repo-setup/

ENV PYTHONPATH=/app/src

RUN chmod +x /tmp/harness-smoke-repo-setup/setup.sh \
    && /tmp/harness-smoke-repo-setup/setup.sh
