#!/bin/bash

mkdir -p /tmp/clamav
freshclam --config-file ./etc/freshclam.conf
poetry install
poetry run pytest -v
