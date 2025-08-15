This project collects security events from CyberArk Privileged Access Management (PAM), transforms them to **Elastic Common Schema (ECS)**, and sends them to **Logstash** for ingestion into Elasticsearch. 

-------------------------------------------------------------

## Features
- **Automated Log Collection**: Fetches security events via CyberArk REST API
- **ECS Normalization**: Converts raw logs to Elastic Common Schema format
- **Secure Delivery**: Supports SSL/TLS encrypted transmission to Logstash
- **Configurable**: YAML-based configuration for easy customization
- **Resilient**: Tracks last collected event to prevent data gaps

---------------------------------------------------------------
## Prerequisites
- Python 3.8+
- CyberArk PAM with REST API access
- Logstash instance (with TCP/HTTP input configured)

---------------------------------------------------------------
## Setup Instructions
1.Install dependencies:

    pip install -r requirements.txt

2.Edit the configuration files:

        -config/config.yaml: Set your CyberArk PVWA URL and credentials

        -config/ecs_mapping.yaml: Customize field mappings as needed
3.run
   
    python -m src.main
