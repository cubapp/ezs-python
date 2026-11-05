# ezs-python and CSV to ODS Converter for EZS

EZS rewrite from perl to python. As simple as possible. 

Plus a Python command-line utility to convert CSV files into LibreOffice Calc (`.ods`) spreadsheets while preserving formulas.

## Prerequisites & Virtual Environment (`uv`)

This project uses [`uv`](https://github.com/astral-sh/uv) for fast package management and running environments.

You can run the tool directly using `uv run`, which automatically handles dependencies.

## Installation & Setup

Make sure you have `uv` installed. If you want to set up the environment manually:

```bash
# Create a virtual environment with uv
uv venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install the required ODF library
uv pip install odfpy
```

## Usage

Run the script by passing the path to your input CSV file as an argument. 

### Basic Usage (Auto-named output)
The output file will automatically have the same name as the input CSV, but with a `.ods` extension.
```bash
uv run convert_csv.py data.csv
```

### Custom Output Filename
Use the optional `-o` (or `--output`) flag to specify a custom name:
```bash
uv run convert_csv.py data.csv -o custom_output.ods
```

### Timestamp in Filename (`-t`)
Use the `-t` flag to automatically append the current date and time to the output filename (e.g., `data-2026.11.27-14.34.ods`):
```bash
uv run convert_csv.py data.csv -t
```

### Debug Mode (`-d`)
Use the `-d` flag to enable verbose logging output for troubleshooting:
```bash
uv run convert_csv.py data.csv -d
```
