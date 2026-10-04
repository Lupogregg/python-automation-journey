import csv
import os
from datetime import datetime
from fleet_functions import check_maintenance_status

def process_csv_and_generate_report(csv_file: str, report_file: str):
    if not os.path.exists(csv_file):
        print(f"Error: Could not find '{csv_file}'.")
        return
    report_lines = []
    report_lines.append("============================================================")
    report_lines.append(f" FLEET MAINTENANCE REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append("============================================================")
    report_lines.append(f"{'ASSET ID':<10} | {'EQUIPMENT NAME':<18} | {'HOURS':<8} | {'STATUS':<15}")
    report_lines.append("-" * 62)
    critical_assets = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            asset_id = row.get('asset_id', 'UNKNOWN')
            name = row.get('name', 'Unknown Item')
            try:
                hours = float(row.get('operating_hours', 0.0))
            except ValueError:
                hours = 0.0
            status, recommendation = check_maintenance_status(hours)
            report_lines.append(f"{asset_id:<10} | {name[:18]:<18} | {hours:<8.1f} | {status:<15}")
            if status in ["SERVICE DUE", "OVERDUE"]:
                critical_assets.append(f"  [!] {asset_id} ({name}): {hours} hrs - {recommendation}")
    report_lines.append("-" * 62)
    if critical_assets:
        report_lines.append("\n*** ACTION REQUIRED ***")
        for action in critical_assets:
            report_lines.append(action)
    else:
        report_lines.append("\nAll equipment is currently operating within acceptable parameters.")
    final_report = "\n".join(report_lines)
    print("\n" + final_report)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(final_report)
    print(f"\n[+] Report successfully saved to: {report_file}")

if __name__ == "__main__":
    process_csv_and_generate_report("machine_data.csv", "maintenance_report.txt")
