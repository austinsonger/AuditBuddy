#!/bin/bash

# Okta
python src/evidence-collection/okta/check_authentication_settings.py
python src/evidence-collection/okta/check_deactivated_users.py
python src/evidence-collection/okta/check_mfa_enrollments.py
python src/evidence-collection/okta/check_password_policies.py
python src/evidence-collection/okta/check_users_and_groups.py

echo "All scripts ran successfully"
