import json
import os
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List, Optional


class EquipmentStatus(str, Enum):
    ACTIVE = "Active"
    MAINTENANCE = "Under Maintenance"
    IDLE = "Idle"
    DECOMMISSIONED = "Decommissioned"


@dataclass
class FleetItem:
    asset_id: str
    name: str
    category: str
    make_model: str
    operating_hours: float = 0.0
    status: str = EquipmentStatus.ACTIVE.value
    last_service_date: str = "N/A"
    location: str = "Yard"
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FleetItem":
        return cls(**data)


class FleetInventoryManager:

    def __init__(self, storage_file: str = "fleet_data.json"):
        self.storage_file = storage_file
        self.inventory: Dict[str, FleetItem] = {}
        self.load_data()

    def load_data(self) -> None:
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, "r") as f:
                raw_data = json.load(f)
                self.inventory = {
                    item_id: FleetItem.from_dict(item_data)
                    for item_id, item_data in raw_data.items()
                }
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading inventory database: {e}")

    def save_data(self) -> None:
        with open(self.storage_file, "w") as f:
            json.dump(
                {
                    item_id: item.to_dict()
                    for item_id, item in self.inventory.items()
                },
                f,
                indent=2,
            )

    def add_item(self, item: FleetItem) -> bool:
        if item.asset_id in self.inventory:
            print(f"Error: Asset ID '{item.asset_id}' already exists.")
            return False
        self.inventory[item.asset_id] = item
        self.save_data()
        return True

    def get_item(self, asset_id: str) -> Optional[FleetItem]:
        return self.inventory.get(asset_id)

    def update_hours(self, asset_id: str, additional_hours: float) -> bool:
        item = self.get_item(asset_id)
        if not item:
            print(f"Asset ID '{asset_id}' not found.")
            return False
        item.operating_hours += additional_hours
        self.save_data()
        return True

    def update_status(
        self,
        asset_id: str,
        new_status: EquipmentStatus,
        service_date: str = "",
    ) -> bool:
        item = self.get_item(asset_id)
        if not item:
            print(f"Asset ID '{asset_id}' not found.")
            return False
        item.status = new_status.value
        if service_date:
            item.last_service_date = service_date
        self.save_data()
        return True

    def list_all(
        self, category_filter: str = "", status_filter: str = ""
    ) -> List[FleetItem]:
        results = list(self.inventory.values())
        if category_filter:
            results = [
                i
                for i in results
                if category_filter.lower() in i.category.lower()
            ]
        if status_filter:
            results = [
                i for i in results if status_filter.lower() in i.status.lower()
            ]
        return results


def print_table(items: List[FleetItem]) -> None:
    if not items:
        print("\nNo matching equipment records found.")
        return

    header = f"{'ID':<10} | {'Name':<20} | {'Category':<15} | {'Hours':<8} | {'Status':<18} | {'Location':<12}"
    divider = "-" * len(header)
    print("\n" + divider)
    print(header)
    print(divider)

    for item in items:
        print(
            f"{item.asset_id:<10} | {item.name[:18]:<20} | {item.category[:13]:<15} | "
            f"{item.operating_hours:<8.1f} | {item.status:<18} | {item.location[:10]:<12}"
        )
    print(divider + "\n")


def interactive_cli():
    manager = FleetInventoryManager()

    while True:
        print("=== FLEET & EQUIPMENT MANAGEMENT SYSTEM ===")
        print("1. View All Equipment")
        print("2. Add New Equipment")
        print("3. Log Operating Hours")
        print("4. Update Equipment Status")
        print("5. Filter Fleet by Category/Status")
        print("6. Exit")

        choice = input("\nSelect option [1-6]: ").strip()

        if choice == "1":
            items = manager.list_all()
            print_table(items)

        elif choice == "2":
            print("\n--- Add New Fleet Asset ---")
            asset_id = (
                input("Asset ID (e.g., PUMP-01, TRK-102): ").strip().upper()
            )
            name = input("Equipment Name: ").strip()
            category = input(
                "Category (Pump, Mixer, Generator, Vehicle): "
            ).strip()
            make_model = input("Make & Model: ").strip()
            hours = float(input("Current Hours [0.0]: ").strip() or "0.0")
            location = input("Current Location [Yard]: ").strip() or "Yard"

            new_item = FleetItem(
                asset_id=asset_id,
                name=name,
                category=category,
                make_model=make_model,
                operating_hours=hours,
                location=location,
            )
            if manager.add_item(new_item):
                print(f"\n[+] Asset {asset_id} added successfully.")

        elif choice == "3":
            print("\n--- Log Working Hours ---")
            asset_id = input("Asset ID: ").strip().upper()
            hours = float(input("Hours to add: ").strip())
            if manager.update_hours(asset_id, hours):
                item = manager.get_item(asset_id)
                print(
                    f"\n[+] Updated {asset_id}. New Total Hours: {item.operating_hours:.1f} hrs"
                )

        elif choice == "4":
            print("\n--- Update Equipment Status ---")
            asset_id = input("Asset ID: ").strip().upper()
            print(
                "Statuses: 1. Active | 2. Under Maintenance | 3. Idle | 4. Decommissioned"
            )
            st_choice = input("Select Status [1-4]: ").strip()

            status_map = {
                "1": EquipmentStatus.ACTIVE,
                "2": EquipmentStatus.MAINTENANCE,
                "3": EquipmentStatus.IDLE,
                "4": EquipmentStatus.DECOMMISSIONED,
            }

            if st_choice in status_map:
                service_date = ""
                if status_map[st_choice] == EquipmentStatus.MAINTENANCE:
                    service_date = input("Service Date (YYYY-MM-DD): ").strip()
                manager.update_status(
                    asset_id, status_map[st_choice], service_date
                )
                print(f"\n[+] Asset {asset_id} status updated.")
            else:
                print("Invalid status choice.")

        elif choice == "5":
            cat = input("Category filter (press Enter to skip): ").strip()
            stat = input("Status filter (press Enter to skip): ").strip()
            items = manager.list_all(category_filter=cat, status_filter=stat)
            print_table(items)

        elif choice == "6":
            print("Exiting Fleet Inventory System. Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    interactive_cli()
