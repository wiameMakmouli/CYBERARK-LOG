This project collects logs from CyberArk Privileged Access Management (PAM), normalizes them to **Elastic Common Schema (ECS)**, and prepares them for ingestion into **Logstash / Elasticsearch**.  

-------------------------------------------------------------

## Features
- Fetch audit logs from CyberArk via REST API.
- Normalize logs to ECS (`@timestamp`, `event`, `user`, `host`, `source`).
- Save logs as JSON for Logstash ingestion.

--------------------------------------------------------------- 

## Project Structure
cyberark-log/
├── config/
│   ├── config.yaml          # Configuration file
│   └── ecs_mapping.yaml     # ECS field mappings
├── src/
│   ├── __init__.py
│   ├── cyberark_client.py   # CyberArk API interactions
│   ├── ecs_mapper.py        # ECS mapping logic
│   ├── logstash_sender.py   # Logstash integration
│   └── main.py             # Main application
├── requirements.txt        # Python dependencies
└── README.md

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