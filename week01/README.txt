Equipment Maintenance CLI
A lightweight Python Command-Line Interface (CLI) tool designed to process fleet operational data from CSV files and evaluate maintenance urgency in real time.

Problem
Tracking service cycles across heavy equipment and fleet machinery via manual logs often leads to missed maintenance intervals, unexpected equipment failure, and operational downtime. Maintenance teams need a rapid, programmatic method to evaluate operating hours across multiple assets without manual calculation.

Solution
The Equipment Maintenance CLI automates status evaluation by reading CSV input logs containing machine IDs and operating hours. It passes each record through custom, reusable logic (fleet_functions.py) and outputs clear, actionable maintenance alerts (SERVICE DUE, SERVICE SOON, or NORMAL) directly to the terminal.

Technologies
Python 3.x – Core scripting language

argparse Module – Command-line interface argument parsing

csv Module (DictReader) – Structured input processing and data manipulation

PowerShell – Automation execution and directory management

Installation
Clone the repository:

PowerShell
git clone https://github.com/YOUR_USERNAME/python-automation-journey.git
Navigate to the week01 directory:

PowerShell
cd python-automation-journey\week01
Verify Python is installed:

PowerShell
python --version
Example Input
Save a CSV file named service_data.csv inside the week01 directory with the following layout:

Code snippet
machine,hours,last_service
SANY-001,1230,2026-06-01
SANY-002,640,2026-08-10
Example Output
Execute the CLI tool in PowerShell by passing the CSV filename:

PowerShell
python maintenance_cli.py service_data.csv
Terminal Output:

Plaintext
SANY-001 -> SERVICE DUE
SANY-002 -> SERVICE SOON
What I Learned
CLI Architecture: Built dynamic terminal tools using Python's native argparse module to handle positional file arguments cleanly.

Robust CSV Parsing: Used csv.DictReader to map header names directly to dictionary keys, combining whitespace stripping (.strip()) and exception handling (try/except ValueError) for numerical type casting.

Modular Code Structure: Separated business logic (fleet_functions.py) from interface execution (maintenance_cli.py) to promote reuse and clean code organization.

Execution Context: Learned how Python resolves module import paths based on the active working directory, resolving ModuleNotFoundError issues in PowerShell.