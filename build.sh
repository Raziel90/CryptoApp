#!/usr/bin/env bash
docker build --build-arg SRV_PORT=8881 -f src/DockerBuild/Dockerfile -t encryption-app .