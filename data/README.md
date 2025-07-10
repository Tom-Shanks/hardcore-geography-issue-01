# Hardcore Geography Data Package
## Denver DIY Venue Displacement Analysis (1995-2025)

### Project Overview
This data package contains comprehensive information about 30+ Denver DIY music venues, their displacement patterns, and the zoning changes that facilitated gentrification. The dataset documents the systematic elimination of cultural spaces through municipal planning policy and real estate speculation.

**License**: MIT License - Open for community use and academic research
**Last Updated**: January 2025
**Data Sources**: Community documentation, planning records, historical archives

---

## Dataset Files

### Primary Dataset
- **`venues_zoning.csv`**: Complete venue database with 30+ locations
- **`venues_zoning.geojson`**: Geographic data for mapping applications
- **`zoning_changes.csv`**: Historical zoning modification records
- **`displacement_analysis.csv`**: Statistical analysis of closure patterns

### Documentation
- **`README.md`**: This documentation file
- **`methodology.md`**: Research methodology and data collection process
- **`field_descriptions.md`**: Detailed field descriptions and data types
- **`usage_examples.md`**: Code examples for data analysis

---

## Data Fields

### Core Venue Information
- **`name`**: Venue name (string)
- **`address`**: Physical address (string)
- **`active_years`**: Operating period (string, format: "YYYY-YYYY" or "YYYY-present")
- **`closure_reason`**: Reason for closure or current status (string)
- **`lat`**: Latitude coordinate (decimal)
- **`lng`**: Longitude coordinate (decimal)
- **`notes`**: Additional context and historical information (string)

### Documentation Status
- **`documentation_status`**: Level of verification and source availability (string)
  - "Active venue" - Currently operating
  - "Documented - [source]" - Verified through specific sources
  - "Research needed" - Requires additional verification

### Zoning Analysis
- **`zoning_type`**: Denver zoning classification code (string)
- **`zoning_description`**: Human-readable zoning description (string)
- **`zoning_year`**: Year of zoning classification (integer)
- **`land_use_change`**: Period of development pressure (string)
  - "Pre-gentrification industrial" - Before 2000
  - "Early mixed-use rezoning" - 2000-2010
  - "Post-recession development" - 2010-2020

### Geographic Analysis
- **`neighborhood`**: Denver neighborhood classification (string)
- **`zoning_density`**: Zoning density score (1-9, higher = more dense)
- **`neighborhood_density`**: Number of venues in neighborhood (integer)
- **`displacement_pattern`**: Risk assessment and closure count (string)

---

## Key Findings

### Displacement Patterns
- **Total Venues**: 30 documented locations
- **Closure Rate**: 43% (13 venues closed)
- **High-Risk Areas**: Central Denver, Downtown, South Broadway
- **Low-Risk Areas**: Colfax corridor, Five Points
- **Average Closure Year**: 2012

### Zoning Analysis
- **Industrial Zones**: 70% of venues operated in areas with <$5/sq ft rent
- **Mixed-Use Rezoning**: 40% higher closure rate in targeted neighborhoods
- **Development Pressure**: Systematic rezoning from industrial to residential

### Geographic Concentration
- **Central Denver**: 13 venues, 4 closures (high risk)
- **South Broadway**: 5 venues, 3 closures (high risk)
- **Colfax**: 6 venues, 0 closures (low risk)
- **RiNo**: 2 venues, 0 closures (protected)

---

## Usage Guidelines

### Academic Research
This dataset is designed for academic research on:
- Urban gentrification and displacement
- Cultural space preservation
- Municipal planning policy analysis
- DIY music scene documentation

### Community Use
The data supports:
- Venue preservation advocacy
- Zoning policy challenges
- Historical documentation
- Community organizing

### Technical Applications
- Interactive mapping
- Statistical analysis
- Policy research
- Historical preservation

---

## Data Quality

### Verification Status
- **Fully Documented**: 15 venues with multiple source verification
- **Partially Documented**: 10 venues with limited sources
- **Research Needed**: 5 venues requiring additional verification

### Geographic Coverage
- **Coordinates Available**: 26/30 venues (87% coverage)
- **Address Verification**: 20/30 venues (67% coverage)
- **Neighborhood Classification**: 30/30 venues (100% coverage)

### Temporal Coverage
- **Earliest Venue**: 1900s (historic venues)
- **Latest Addition**: 2016 (current DIY spaces)
- **Active Period**: 1995-2025 (primary analysis period)

---

## Methodology

### Data Collection
1. **Community Documentation**: Interviews with venue operators and musicians
2. **Historical Archives**: Newspaper articles, flyer collections, oral histories
3. **Planning Records**: Zoning changes, development applications
4. **Field Research**: Site visits and neighborhood documentation

### Verification Process
1. **Primary Sources**: Direct interviews and documentation
2. **Secondary Sources**: Newspaper articles, online archives
3. **Cross-Reference**: Multiple source verification
4. **Community Review**: Local expert validation

### Analysis Framework
1. **Spatial Analysis**: Geographic concentration and displacement patterns
2. **Temporal Analysis**: Timeline of closures and development pressure
3. **Policy Analysis**: Zoning changes and planning decisions
4. **Statistical Analysis**: Closure rates and risk assessment

---

## Citation

When using this dataset, please cite:

```
Hardcore Geography Project. 2025. "Denver DIY Venue Displacement Database." 
Sonic Archaeology of Denver's DIY Displacement. 
Available: https://github.com/hardcore-geography/denver-venues
```

---

## Contributing

### Data Corrections
- Submit corrections through GitHub issues
- Include source documentation
- Provide contact information for verification

### Additional Venues
- Include complete venue information
- Provide source documentation
- Follow established data format

### Documentation Improvements
- Enhance field descriptions
- Add usage examples
- Improve methodology documentation

---

## Technical Specifications

### File Formats
- **CSV**: UTF-8 encoding, comma-separated
- **GeoJSON**: WGS84 coordinate system
- **Documentation**: Markdown format

### Data Types
- **Strings**: Venue names, addresses, descriptions
- **Integers**: Years, density scores, venue counts
- **Decimals**: Latitude/longitude coordinates
- **Categories**: Zoning types, neighborhoods, status

### Quality Standards
- **Accuracy**: Cross-referenced with multiple sources
- **Completeness**: 87% geographic coverage
- **Consistency**: Standardized field formats
- **Accessibility**: Open format, clear documentation

---

## Contact Information

**Project Lead**: Hardcore Geography Research Team
**Email**: [contact information]
**Repository**: https://github.com/hardcore-geography/denver-venues
**License**: MIT License

---

## Acknowledgments

- Denver DIY music community
- Historical venue operators and musicians
- Planning department records
- Community archives and documentation
- Academic research partners

This dataset represents collaborative research between academic analysis and community knowledge, documenting the systematic displacement of cultural spaces through gentrification and municipal planning policy.