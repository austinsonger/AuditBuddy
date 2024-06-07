#!/bin/bash

python src/evidence-collection/okta/check_authentication_settings.py

python src/evidence-collection/okta/check_users_and_groups.py

echo "All scripts ran successfully"
