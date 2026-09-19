# Harness Smoke runtime image: OpenCode
#
# This image contains OpenCode and the runtime assumptions made by Harbor's
# stock OpenCode integration. Task repositories/verifiers are layered on top.
FROM python:3.12-slim

ARG NVM_VERSION=v0.40.2
ARG NODE_MAJOR=22
ARG OPENCODE_VERSION=1.18.30

ENV DEBIAN_FRONTEND=noninteractive \
    NVM_DIR=/root/.nvm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        coreutils \
        curl \
        git \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Match Harbor's stock OpenCode runtime convention: NVM under $HOME/.nvm,
# Node 22 as the default alias, and a global opencode-ai package.
RUN curl -fsSL "https://raw.githubusercontent.com/nvm-sh/nvm/${NVM_VERSION}/install.sh" \
        | env -u NODE_VERSION bash \
    && . "$NVM_DIR/nvm.sh" \
    && nvm install "$NODE_MAJOR" \
    && nvm alias default "$NODE_MAJOR" \
    && npm install -g "opencode-ai@${OPENCODE_VERSION}" \
    && node --version \
    && npm --version \
    && opencode --version

WORKDIR /app
