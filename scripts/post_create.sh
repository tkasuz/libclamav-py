#!/bin/bash

mkdir -p /tmp/clamav
freshclam --config-file ./freshclam.conf
poetry install
poetry run pytest -v
