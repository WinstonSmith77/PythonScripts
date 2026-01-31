import time
import argparse
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Write current time to a file every 10 seconds')
    parser.add_argument('file', type=str, help='Path to the output text file')
    args = parser.parse_args()
    
    output_file = Path(args.file)
    
    print(f"Writing time to {output_file} every 10 seconds. Press Ctrl+C to stop.")
    
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with output_file.open('a') as f:
                f.write(f"{current_time}\n")
            print(f"Wrote: {current_time}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
