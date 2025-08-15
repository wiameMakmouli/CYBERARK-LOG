import yaml
import time
import logging
from pathlib import Path
from .cyberark_client import CyberArkClient
from .ecs_mapper import ECSMapper
from .logstash_sender import LogstashSender

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_config():
    with open(Path(__file__).parent.parent / "config/config.yaml") as f:
        return yaml.safe_load(f)

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    config = load_config()

    cyberark = CyberArkClient(config)
    mapper = ECSMapper(Path(__file__).parent.parent / "config/ecs_mapping.yaml")
    logstash = LogstashSender(config)

    logger.info("Starting CyberArk Log Collector")
    try:
        while True:
            events = cyberark.get_security_events()
            if events:
                logger.info(f"Processing {len(events)} events")
                for event in events:
                    ecs_event = mapper.map_to_ecs(event)
                    if not logstash.send(ecs_event):
                        logger.error(f"Failed to send event: {event.get('EventID')}")
            
            time.sleep(config['settings']['polling_interval'])
    except KeyboardInterrupt:
        logger.info("Shutting down")

if __name__ == "__main__":
    main()