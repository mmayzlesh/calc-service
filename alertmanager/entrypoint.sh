#!/bin/sh

# Directly use /etc/alertmanager/alertmanager.yml for substitution.
# Using a temporary file to avoid potential issues with simultaneous read and write.
envsubst < /etc/alertmanager/alertmanager.yml > /tmp/alertmanager_temp.yml

# Overwrite the original with the substituted version.
mv /tmp/alertmanager_temp.yml /etc/alertmanager/alertmanager.yml

# Run Alertmanager.
exec /bin/alertmanager "$@"
