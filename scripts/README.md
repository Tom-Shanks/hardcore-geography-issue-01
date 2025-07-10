# Data Processing Scripts

This directory contains automation scripts for processing venue data and maintaining data quality.

## Scripts

### `validate_venues.py`
Validates venue database for data quality and completeness.

**Usage:**
```bash
python scripts/validate_venues.py data/raw/hg-01-venues-raw.csv
```

**Features:**
- Validates coordinate accuracy for Denver area
- Checks year range formatting
- Identifies missing required fields
- Generates validation report with statistics

**Output:**
- Validation report to console
- Optional clean CSV output with `--output` flag

### Requirements

Python 3.6+ with standard library (no external dependencies required)

## Development Guidelines

- All scripts should include docstrings and type hints
- Follow PEP 8 style guidelines
- Include error handling for file operations
- Generate meaningful output/logs
- Document usage and examples

## Future Scripts

Planned automation tools:
- `geocode_venues.py` - Batch geocoding for missing coordinates
- `export_geojson.py` - Convert venue data to GeoJSON
- `validate_zoning.py` - Cross-reference venues with zoning data
- `generate_reports.py` - Create summary reports and visualizations