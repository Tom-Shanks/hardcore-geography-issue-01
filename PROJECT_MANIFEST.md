# PROJECT MANIFEST
## Hardcore Geography – Issue 01

### Project Overview
A 32-page half-letter zine, blog, and podcast documenting how zoning, speculation, and culture-washing displaced Denver's DIY punk venues (1995-2025).

### Role Matrix
| Role | Responsibilities | Deliverables |
|------|-----------------|--------------|
| Research Lead | Data collection, venue documentation, zoning analysis | venues_raw.csv, zoning_shapefile_index.md |
| Content Creator | Writing, editing, narrative development | Article drafts, podcast scripts |
| Design Lead | Layout, typography, visual identity | Zine layouts, style guide implementation |
| Audio Producer | Podcast recording, editing, sound design | Audio files, Reaper projects |
| Web Developer | Site development, content management | Static site, blog posts |

### Milestones
- [ ] **Phase 1: Research & Data Collection**
  - Venue database compilation
  - Zoning data acquisition
  - Bibliography development
  - Flyer/artifact scraping
- [ ] **Phase 2: Content Development**
  - Article drafts
  - Podcast recording
  - Image processing
  - Citation formatting
- [ ] **Phase 3: Production**
  - Zine layout design
  - Audio post-production
  - Web site deployment
  - Final review & publication

### Style Rules
1. **Typography**: League Gothic Condensed headers, PT Mono 9.5pt body text
2. **Citations**: Chicago author–date format throughout
3. **Punctuation**: NO EM DASHES — use colons, slashes, or en-dashes instead
4. **Color Palette**: Grayscale + single spot-color only
5. **Accessibility**: Alt-text required for every image
6. **File Naming**: snake_case for data files, kebab-case for content

### Technical Specifications
- **Zine Format**: Half-letter (5.5" x 8.5"), 32 pages
- **Audio Format**: 44.1kHz/16-bit WAV masters, MP3 distribution
- **Web Platform**: Static site generation
- **Data Formats**: CSV for tabular data, JSON for bibliography, Markdown for content

### Quality Standards
- All sources must be cited using Chicago author–date format
- All images require descriptive alt-text
- Data files must include metadata headers
- Code must include inline documentation
- Content must maintain journalistic objectivity while acknowledging perspective

### Workflow
1. **Research**: Collect data in `/data/raw`, document sources in `/data/sources`
2. **Scripts**: Automation tools in `/scripts` with clear documentation
3. **Content**: Draft materials in `/site/content`, final layouts in `/zine`
4. **Audio**: Reaper projects in `/audio/reaper`, exports to `/audio`
5. **Assets**: All images and graphics in `/assets/img` with alt-text metadata

### Review Process
- Peer review required for all historical claims
- Fact-checking against primary sources
- Style guide compliance check before final production
- Accessibility audit for web and print materials