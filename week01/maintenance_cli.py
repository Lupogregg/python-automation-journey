import csv
import argparse
import os
import sys

# Import the rules you already built
from fleet_functions import check_maintenance_status

def process_file(filepath: str):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        # Ensure the required columns exist
        if 'machine' not in reader.fieldnames or 'hours' not in reader.fieldnames:
            print("Error: CSV must contain 'machine' and 'hours' columns.")
            sys.exit(1)

        for row in reader:
            machine = row['machine'].strip()
            try:
                hours = float(row['hours'].strip())
            except ValueError:
                hours = 0.0
            
            # We only need the status, we can ignore the recommendation string
            status, _ = check_maintenance_status(hours)
            
            print(f"{machine} -> {status}")

def main():
    parser = argparse.ArgumentParser(description="Equipment Maintenance CLI")
    parser.add_argument("file", help="Path to the CSV file (e.g., service_data.csv)")
    args = parser.parse_args()

    process_file(args.file)

if __name__ == "__main__":
    main()
