# Denver Zoning Data Sources

## Primary Data Sources

### City and County of Denver Open Data Portal
- **URL**: https://opendata-geospatialdenver.hub.arcgis.com
- **Department**: Community Planning and Development
- **Data Type**: Zoning classifications, boundary shapefiles

### Denver GIS Data Portal
- **URL**: https://www.denvergov.org/Government/Departments/Technology-Services/Geographic-Information-Systems-GIS
- **Data Type**: Zoning shapefiles, land use classifications
- **Format**: Shapefile, GeoJSON, KML

## Specific Datasets Required

### Zoning Classifications
- **Dataset**: Current zoning districts
- **Coverage**: City and County of Denver
- **Update Frequency**: As amended by City Council
- **Spatial Reference**: State Plane Colorado Central (EPSG:3502)

### Historic Zoning Data
- **Dataset**: Zoning changes over time
- **Coverage**: 1995-2025 (project timeframe)
- **Status**: May require records requests for historical data

## Data Acquisition Methods

### Direct Download
1. Access Denver Open Data Portal
2. Search for "zoning" or "land use" datasets
3. Download in preferred format (Shapefile recommended)
4. Verify spatial reference system

### API Access
- **Base URL**: https://www.denvergov.org/media/gis/DataCatalog/
- **Format**: REST API endpoints available
- **Authentication**: Public access, no API key required

### Records Requests
- For historical zoning data not available online
- Contact: Community Planning and Development
- Processing time: 3-10 business days

## Processing Notes

- Convert all data to WGS84 (EPSG:4326) for web mapping
- Maintain original State Plane coordinates for accuracy
- Document all transformations and processing steps
- Validate against known venue locations

## Status
- 📋 Initial portal research completed
- 📋 Dataset identification in progress
- 📋 Download and processing pending