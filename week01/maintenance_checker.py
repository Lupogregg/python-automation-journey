import sys
from dataclasses import dataclass
from enum import Enum


class MaintenanceStatus(str, Enum):
    NORMAL = "NORMAL"
    SERVICE_SOON = "SERVICE SOON"
    SERVICE_DUE = "SERVICE DUE"
    OVERDUE = "OVERDUE"


@dataclass
class MaintenanceReport:
    hours: float
    status: MaintenanceStatus
    description: str


def evaluate_maintenance_status(hours: float) -> MaintenanceReport:
    if hours < 0:
        raise ValueError("Operating hours cannot be negative.")

    if hours < 500:
        return MaintenanceReport(
            hours=hours,
            status=MaintenanceStatus.NORMAL,
            description="Equipment is in optimal operating condition.",
        )
    elif 500 <= hours < 1000:
        return MaintenanceReport(
            hours=hours,
            status=MaintenanceStatus.SERVICE_SOON,
            description="Schedule routine servicing during upcoming downtime.",
        )
    elif 1000 <= hours < 1500:
        return MaintenanceReport(
            hours=hours,
            status=MaintenanceStatus.SERVICE_DUE,
            description="Maintenance required. Book service slot immediately.",
        )
    else:
        return MaintenanceReport(
            hours=hours,
            status=MaintenanceStatus.OVERDUE,
            description="CRITICAL: Equipment exceeded maximum safe service interval!",
        )


def main():
    print("=== EQUIPMENT MAINTENANCE STATUS CHECKER ===")
    try:
        raw_input = input("Enter operating hours (e.g., 650): ").strip()
        hours = float(raw_input)
        report = evaluate_maintenance_status(hours)

        print("\n" + "=" * 45)
        print(f" OPERATING HOURS : {report.hours:,.1f} hrs")
        print(f" STATUS          : [{report.status.value}]")
        print(f" RECOMMENDATION  : {report.description}")
        print("=" * 45 + "\n")

    except ValueError as e:
        print(f"\n[Error] Invalid input: {e}. Please enter a valid numerical value.")


if __name__ == "__main__":
    main()
