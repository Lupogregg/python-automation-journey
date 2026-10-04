import argparse
import sys
from dataclasses import dataclass

@dataclass
class EquipmentCostModel:
    name: str
    capex: float                 # Upfront purchase cost ($)
    lifespan_years: float        # Expected service life in years
    annual_maintenance: float   # Service/maintenance contracts per year ($)
    power_watts: float          # Power draw in Watts (0 for unpowered service)
    electricity_rate_kwh: float # Cost per kWh ($)
    daily_hours: float          # Usage hours per day
    days_per_year: float = 365.0 # Days of operation per year

    @property
    def annual_power_kwh(self) -> float:
        return (self.power_watts / 1000.0) * self.daily_hours * self.days_per_year

    @property
    def annual_power_cost(self) -> float:
        return self.annual_power_kwh * self.electricity_rate_kwh

    @property
    def annual_opex(self) -> float:
        return self.annual_maintenance + self.annual_power_cost

    @property
    def total_cost_ownership(self) -> float:
        return self.capex + (self.annual_opex * self.lifespan_years)

    @property
    def total_operating_hours(self) -> float:
        return self.daily_hours * self.days_per_year * self.lifespan_years

    @property
    def cost_per_hour(self) -> float:
        return self.total_cost_ownership / self.total_operating_hours if self.total_operating_hours > 0 else 0.0

    @property
    def annual_depreciation(self) -> float:
        return self.capex / self.lifespan_years if self.lifespan_years > 0 else 0.0

def display_report(model: EquipmentCostModel) -> None:
    print("\n" + "=" * 50)
    print(f" EQUIPMENT COST ANALYSIS: {model.name.upper()}")
    print("=" * 50)
    print(f"  Upfront CapEx              : ${model.capex:,.2f}")
    print(f"  Expected Lifespan           : {model.lifespan_years:.1f} years")
    print(f"  Annual Straight Depreciation: ${model.annual_depreciation:,.2f} / yr")
    print("-" * 50)
    print(f"  Annual Maintenance/Service  : ${model.annual_maintenance:,.2f} / yr")
    print(f"  Annual Electricity Usage    : {model.annual_power_kwh:,.1f} kWh")
    print(f"  Annual Electricity Cost     : ${model.annual_power_cost:,.2f} / yr")
    print(f"  Total Annual OpEx           : ${model.annual_opex:,.2f} / yr")
    print("-" * 50)
    print(f"  Total Cost of Ownership (TCO): ${model.total_cost_ownership:,.2f}")
    print(f"  Cost per Operating Hour     : ${model.cost_per_hour:,.2f} / hr")
    print("=" * 50 + "\n")

def prompt_float(prompt_text: str, default: float = 0.0) -> float:
    raw = input(f"{prompt_text} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        print("Invalid number, using default.")
        return default

def interactive_mode() -> EquipmentCostModel:
    print("\n--- Interactive Equipment Cost Calculator ---")
    name = input("Equipment/Service Name [Server Array]: ").strip() or "Server Array"
    capex = prompt_float("Upfront Purchase Price ($)", 5000.0)
    lifespan = prompt_float("Lifespan in Years", 5.0)
    maintenance = prompt_float("Annual Service/Maintenance Contract ($)", 600.0)
    power = prompt_float("Power consumption in Watts", 450.0)
    rate = prompt_float("Electricity rate ($ per kWh)", 0.15)
    hours = prompt_float("Daily usage hours", 24.0)
    days = prompt_float("Days used per year", 365.0)

    return EquipmentCostModel(
        name=name,
        capex=capex,
        lifespan_years=lifespan,
        annual_maintenance=maintenance,
        power_watts=power,
        electricity_rate_kwh=rate,
        daily_hours=hours,
        days_per_year=days
    )

def main():
    parser = argparse.ArgumentParser(description="CLI Equipment & Service-Cost Calculator")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run interactive prompt mode")
    parser.add_argument("--name", type=str, default="Equipment Item", help="Name of equipment/service")
    parser.add_argument("--capex", type=float, help="Upfront cost ($)")
    parser.add_argument("--lifespan", type=float, help="Lifespan in years")
    parser.add_argument("--maintenance", type=float, default=0.0, help="Annual maintenance cost ($)")
    parser.add_argument("--watts", type=float, default=0.0, help="Power rating in Watts")
    parser.add_argument("--kwh-rate", type=float, default=0.15, help="Cost per kWh ($)")
    parser.add_argument("--daily-hours", type=float, default=8.0, help="Operating hours per day")
    parser.add_argument("--days-per-year", type=float, default=250.0, help="Operating days per year")

    args = parser.parse_args()

    # If flags are missing or --interactive is passed, launch interactive prompt
    if args.interactive or args.capex is None or args.lifespan is None:
        model = interactive_mode()
    else:
        model = EquipmentCostModel(
            name=args.name,
            capex=args.capex,
            lifespan_years=args.lifespan,
            annual_maintenance=args.maintenance,
            power_watts=args.watts,
            electricity_rate_kwh=args.kwh_rate,
            daily_hours=args.daily_hours,
            days_per_year=args.days_per_year
        )

    display_report(model)

if __name__ == "__main__":
    main()