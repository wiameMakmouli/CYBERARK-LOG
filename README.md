This project collects logs from CyberArk Privileged Access Management (PAM), normalizes them to **Elastic Common Schema (ECS)**, and prepares them for ingestion into **Logstash / Elasticsearch**.  

-------------------------------------------------------------

## Features
- Fetch audit logs from CyberArk via REST API.
- Normalize logs to ECS (`@timestamp`, `event`, `user`, `host`, `source`).
- Save logs as JSON for Logstash ingestion.

--------------------------------------------------------------- 

## Project Structure
cyberark-log-pipeline/
    ├── main.py                # Main script to run the pipeline
    ├── config.py              # Configuration file
    ├── fetcher/               # Module for fetching logs
    │     └── cyberark_fetcher.py
    ├── normalizer/            # Module for ECS normalization
    │     └── ecs_normalizer.py
    ├── utils/                 # Helper functions
    │     └── file_writer.py
    ├── requirements.txt       # Python dependencies
    └── README.md

---------------------------------------------------------------

## Setup Instructions
1.Install dependencies:

    pip install -r requirements.txt

2.Edit config.py:

    -Set CYBERARK_URL to your CyberArk API endpoint.

    -Set API_TOKEN to your CyberArk API token.

    -Set OUTPUT_FILE to the desired JSON output path.

3.run
   
     python main.py