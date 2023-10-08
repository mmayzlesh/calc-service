#!/bin/bash
set -e

# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add bokysan https://bokysan.github.io/docker-postfix/
helm repo update

# Build Docker image
docker build -t calc-app:1 .

# Install Redis
helm install redis bitnami/redis -f calc-app/redis-values.yaml

# Install calc-app
helm install calc-app ./calc-app

# Upgrade/Install Postfix Mail
helm upgrade --install --set persistence.enabled=false --set config.general.ALLOWED_SENDER_DOMAINS=749ep.site postfix bokysan/mail

# Install Prometheus
helm install prometheus prometheus-community/prometheus -f calc-app/prometheus-values.yaml
