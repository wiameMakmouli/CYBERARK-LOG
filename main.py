from fetcher.cyberark_fetcher import fetch_cyberark_logs
from normalizer.ecs_normalizer import normalize_to_ecs
from utils.file_writer import write_json_logs
from config import OUTPUT_FILE

def main():
    raw_logs = fetch_cyberark_logs()
    ecs_logs = [normalize_to_ecs(log) for log in raw_logs]
    write_json_logs(ecs_logs, OUTPUT_FILE)

if __name__ == "__main__":
    main()
