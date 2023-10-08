# calc-service

This repository contains the configurations and code for deploying Your Project Name. The system can be deployed using either Docker Compose or Helm, providing flexibility based on your deployment needs.

## Prerequisites
- Docker and Docker Compose installed (for Docker Compose deployment).
- Kubernetes cluster and Helm installed (for Helm deployment).

## Getting Started
1. Clone this repository to your local machine:
```
git clone https://github.com/mmayzlesh/calc-service.git
```
2. Configure email address:
- Create a no-strict verification temp email, for instance using mail.tm (Gmail will not work due to missing DKIM verification).
- Update the created email address in the configuration:
    - For Docker Compose deployment: Update alertmanager/alertmanager.yml in the "to" section.
    - For Helm deployment: Update calc-app/prometheus-values.yaml in the "to" section.

### Deployment: Using Docker Compose
Navigate to the directory where docker-compose.yml is located.

Run the application using:

```
docker-compose up
```

Once the services are up, you can access them at:

- calc-app: http://localhost:8080
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093

### Deployment: Using Helm
Ensure Helm is set up correctly on your machine.

Run the installation script:
```
./install-with-helm.sh
```

Pleae note that with helm deployment it might take some time for all the resources to start.

After the deployment, you can access the services at:

- calc-app: http://localhost:30080
- Prometheus: http://localhost:30900
- Alertmanager: http://localhost:30903

## Architecture
- Redis: Used to store and persist data.
- Core System: Serves the API using Gunicorn.
- Postfix: Acts as an SMTP server.
- Prometheus and Alertmanager: Used to scrape metrics and send notifications based on predefined rules.

## Email Configuration
Emails will be sent from 749ep.site domain (configurable).

## Endpoints
**/** - Returns access time of the local machine formatted as UTC.

**/calculate** - Accepts two numbers and an operator (either 'sum' or 'product') and returns the result.

**/results** - Returns a list of saved calculation results as key-value pairs.

**/results/\<key\>** - Deletes the provided key and its values from the results list.

**/metrics** - Address for Prometheus to scrape the system metrics

In addition to the above, there are health and readiness endpoints utilized by Kubernetes.
