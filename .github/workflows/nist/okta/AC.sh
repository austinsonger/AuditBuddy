#!/bin/bash

python src/evidence-collection/okta/check_deactivated_users.py
python src/evidence-collection/okta/check_mfa_enrollments.py
python src/evidence-collection/okta/check_password_policies.py


echo "All scripts ran successfully"
