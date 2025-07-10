# Flyer Archive Documentation

## Directory Structure

```
assets/flyers/
├── 1990s/          # Flyers from 1990-1999
├── 2000s/          # Flyers from 2000-2009
├── 2010s/          # Flyers from 2010-2019
├── 2020s/          # Flyers from 2020-present
└── README.md       # This file
```

## Naming Convention

Format: `YYYY-MM-venue-event.jpg`

### Examples:
- `1998-03-monkey-mania-punk-show.jpg`
- `2005-12-kingdom-of-doom-new-years.jpg`
- `2016-08-rhinoceropolis-noise-fest.jpg`

### Special Cases:
- Multiple events same day: `YYYY-MM-DD-venue-event-01.jpg`, `YYYY-MM-DD-venue-event-02.jpg`
- Unknown dates: `YYYY-00-venue-event.jpg` (unknown month)
- Estimated dates: `YYYY-MM-venue-event-est.jpg`

## Scanning Standards

### Technical Requirements
- **Resolution**: 300 DPI minimum for archival quality
- **Format**: JPEG for web use, TIFF for archival masters
- **Color Mode**: RGB for color flyers, Grayscale for B&W
- **File Size**: Balance quality vs. web performance

### Scanning Process
1. **Preparation**: Clean scanner bed, handle flyers carefully
2. **Scanning**: Scan at 600 DPI, downsample to 300 DPI if needed
3. **Processing**: Minimal correction, preserve authentic appearance
4. **Archival**: Save unprocessed TIFF master + processed JPEG web copy

### Metadata Documentation
For each flyer, document:
- **Date**: Event date (YYYY-MM-DD)
- **Venue**: Primary venue name
- **Event**: Event name or description
- **Bands**: Performing artists
- **Promoter**: Event organizer (if known)
- **Source**: How/where flyer was obtained
- **Rights**: Copyright/usage permissions

## File Organization

### Master Files
- Store original scans as TIFF files
- Archive in separate `/masters/` directory
- Keep original filename references

### Web-Ready Files
- JPEG format for web display
- Optimized for loading speed
- Follow naming convention exactly

## Quality Control

### Image Standards
- Sharp focus, no blur or distortion
- Proper exposure, readable text
- Accurate color reproduction
- Consistent orientation

### Documentation Standards
- All metadata fields completed
- Venue names match database spellings
- Dates verified against multiple sources
- Source attribution documented

## Current Status

- 📋 Directory structure created
- 📋 Naming conventions established
- 📋 Scanning standards documented
- 📋 Initial flyer collection pending
- 📋 Metadata template to be created

## Usage Guidelines

1. **Research**: Verify venue/event details before filing
2. **Consistency**: Use standardized venue names from database
3. **Preservation**: Handle original flyers with care
4. **Attribution**: Document sources and permissions
5. **Access**: Maintain both archival and web-ready versions

*Last updated: 2024*