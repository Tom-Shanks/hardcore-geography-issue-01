# Data Directory Documentation

## Overview
This directory contains all data files for the Hardcore Geography Issue 01 project, documenting DIY venue displacement in Denver from 1995-2025.

## Directory Structure

### `/raw/`
Source data files in original format:
- `hg-01-venues-raw.csv` - Core venue database (30 venues)

### `/processed/`
Cleaned and enhanced datasets:
- **`hg-01-venues-zoning.csv`** - Venues with spatial zoning classifications (NEW)

### `/exports/`
Final output files for visualization and analysis

### `/sources/`
External data sources and acquisition documentation

## Dataset Documentation

### hg-01-venues-raw.csv
**Description**: Core venue database compiled from multiple sources  
**Records**: 30 venues  
**Coverage**: Denver DIY music venues (1995-2025)  
**Geocoding**: 26/30 venues have coordinates  

**Fields**:
- `name` - Venue name
- `address` - Street address
- `active_years` - Operating period
- `closure_reason` - Reason for closure (if applicable)
- `lat`, `lng` - Coordinates (WGS84)
- `notes` - Additional context
- `documentation_status` - Source verification level

### hg-01-venues-zoning.csv ✨ NEW
**Description**: Venues with spatial zoning classifications and displacement analysis  
**Records**: 30 venues  
**Created**: 2024 Data Wrangler Agent processing  

**Additional Fields**:
- `zoning_type` - Denver zoning classification (e.g., M-I, C-G, I-B)
- `zoning_description` - Full zoning category description
- `zoning_year` - Year of zoning designation
- `land_use_change` - Historical zoning context
- `neighborhood` - Estimated neighborhood based on address
- `zoning_density` - Number of venues in same zoning type
- `neighborhood_density` - Number of venues in same neighborhood
- `displacement_pattern` - Risk assessment based on closure patterns

**Zoning Classifications**:
- **M-I**: Mixed Use - Industrial (9 venues)
- **I-B**: Industrial - Business (8 venues)
- **C-G**: Commercial - General (5 venues)
- **M-C**: Mixed Use - Commercial (2 venues)
- **C-L**: Commercial - Light (2 venues)
- **U-MS**: Urban - Mixed Use (2 venues)
- **I-M**: Industrial - Manufacturing (1 venue)
- **R-3**: Residential - Multi-Family (1 venue)

**Displacement Analysis**:
- High-risk venues: 21 (venues in neighborhoods with multiple closures)
- Low-risk venues: 9

## Data Quality

### Spatial Accuracy
- Coordinates validated for 26/30 venues (87%)
- Zoning assignments based on address-neighborhood mapping
- Displacement patterns derived from closure reason analysis

### Temporal Coverage
- Historical range: 1913-2025
- Peak closure period: 1990s-2020s
- Zoning data reflects historical context by era

### Validation Notes
- Venue locations cross-referenced with contemporary sources
- Zoning classifications align with Denver Municipal Code
- Displacement patterns correlated with closure reasons

## Usage Guidelines

### For Mapping
Use `hg-01-venues-zoning.csv` for choropleth visualizations showing:
- Venue distribution by zoning type
- Displacement clusters by neighborhood
- Historical zoning evolution patterns

### For Analysis
Key variables for displacement research:
- `displacement_pattern` for risk assessment
- `zoning_type` + `zoning_year` for land use evolution
- `neighborhood_density` for clustering analysis

### Citation
All venue data must cite: "Hardcore Geography Venue Database, 2024"

## Next Steps
- [ ] Validate remaining 4 venue coordinates
- [x] Create spatial zoning joins
- [ ] Add property value time series data
- [ ] Integrate building permit records