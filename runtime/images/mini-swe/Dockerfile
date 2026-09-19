# Harness Smoke runtime image: Mini-SWE-Agent
#
# This image contains the harness and its own runtime dependencies only.
# Task-specific repositories/instructions/verifiers are layered separately.
FROM python:3.12-slim

ARG MINI_SWE_VERSION=2.4.6
ARG UV_VERSION=0.7.13

ENV DEBIAN_FRONTEND=noninteractive \
    UV_TOOL_DIR=/opt/uv-tools \
    UV_TOOL_BIN_DIR=/usr/local/bin \
    PATH=/usr/local/bin:${PATH}

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir "uv==${UV_VERSION}"

RUN uv tool install "mini-swe-agent==${MINI_SWE_VERSION}" --with 'litellm[proxy]' \
    && command -v mini-swe-agent \
    && mini-swe-agent --help >/dev/null \
    && uv tool list | grep '^mini-swe-agent '

# Harbor coding tasks normally operate in the task workdir.
WORKDIR /app
