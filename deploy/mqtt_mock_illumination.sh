#!/bin/bash
DIRNAME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONFNAME="broker.conf"

cd "${DIRNAME}"
cd ..
pipenv run python3 -m intervention_system.tests.mqtt_clients.mock_illumination --config settings_localhost.json
