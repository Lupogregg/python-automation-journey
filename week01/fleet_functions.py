import json
import os

def calculate_annual_power_cost(watts: float, daily_hours: float, days_per_year: float, kwh_rate: float) -> float:
    kwh_per_year = (watts / 1000.0) * daily_hours * days_per_year
    return kwh_per_year * kwh_rate

def calculate_equipment_costs(capex: float, lifespan: float, annual_maintenance: float, power_cost: float) -> dict:
    annual_opex = annual_maintenance + power_cost
    tco = capex + (annual_opex * lifespan)
    return {
        "annual_opex": annual_opex,
        "total_cost_ownership": tco,
        "annual_depreciation": capex / lifespan if lifespan > 0 else 0.0
    }

def check_maintenance_status(hours: float) -> tuple:
    if hours < 500:
        return "NORMAL", "Equipment is in optimal condition."
    elif 500 <= hours < 1000:
        return "SERVICE SOON", "Schedule routine servicing."
    elif 1000 <= hours < 1500:
        return "SERVICE DUE", "Maintenance required. Book immediately."
    else:
        return "OVERDUE", "CRITICAL: Exceeded safe service interval!"

def load_inventory(filepath: str = "fleet_data.json") -> dict:
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_inventory(inventory_dict: dict, filepath: str = "fleet_data.json") -> None:
    with open(filepath, "w") as f:
        json.dump(inventory_dict, f, indent=2)

def add_equipment(inventory_dict: dict, asset_id: str, name: str, category: str) -> str:
    if asset_id in inventory_dict:
        return f"Error: Asset {asset_id} already exists."
    inventory_dict[asset_id] = {
        "name": name,
        "category": category,
        "operating_hours": 0.0,
        "status": "NORMAL"
    }
    return f"Success: Asset {asset_id} added."

def log_working_hours(inventory_dict: dict, asset_id: str, hours_to_add: float) -> str:
    if asset_id not in inventory_dict:
        return f"Error: Asset {asset_id} not found."
    current_hours = inventory_dict[asset_id].get("operating_hours", 0.0)
    new_hours = current_hours + hours_to_add
    inventory_dict[asset_id]["operating_hours"] = new_hours
    status, recommendation = check_maintenance_status(new_hours)
    inventory_dict[asset_id]["status"] = status
    return f"Updated {asset_id} to {new_hours} hrs. Status is now: {status}."
