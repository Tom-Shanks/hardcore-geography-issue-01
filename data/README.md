# Data Directory Documentation

## Directory Structure

```
data/
├── raw/           # Source files and unprocessed data
├── processed/     # Cleaned and validated datasets
├── exports/       # Final outputs for publication
└── README.md      # This file
```

## Data Sources

### Venue Database (`hg-01-venues-raw.csv`)
- **Primary Source**: Manual research and compilation
- **Coverage**: Denver DIY/punk venues, 1995-2025
- **Status**: 30 venues documented, ongoing research
- **Fields**: name, address, active_years, closure_reason, lat, lng, notes, documentation_status

### Zoning Data
- **Source**: Denver Open Data Portal
- **Format**: Shapefile/GeoJSON
- **Coverage**: City and County of Denver zoning classifications
- **Status**: Research in progress

## Processing Workflow

1. **Raw Data Collection**: Store original source files in `/raw/`
2. **Data Cleaning**: Process and validate data, output to `/processed/`
3. **Final Exports**: Generate publication-ready datasets in `/exports/`
4. **Documentation**: Maintain source documentation and processing scripts

## Quality Standards

- All geographic coordinates in WGS84 (EPSG:4326)
- Date formats: YYYY-MM-DD or YYYY-YYYY for ranges
- CSV files must include metadata headers
- All processing steps documented in `/scripts/`

## Current Status

- ✅ Initial venue database (30 entries)
- 🔄 Zoning data acquisition in progress
- 📋 Additional venues being researched
- 📋 Geocoding verification needed for some entries