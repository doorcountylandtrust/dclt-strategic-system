# DCLT Strategic System - Scripts Organization
*Updated: 2025-09-11*

## Directory Structure

The scripts have been organized into logical categories for better maintainability and discoverability:

```
scripts/
├── data_migration/           # Scripts for data processing and migration
├── notion_processing/        # Notion export processing and cleanup  
├── screenshot_optimization/  # Screenshot quality management
├── system_setup/            # System configuration and validation
└── [existing analysis scripts] # Strategic analysis and reporting tools
```

## Script Categories

### 📁 `data_migration/`
Scripts for processing and migrating data between systems.

| Script | Purpose | Usage |
|--------|---------|--------|
| `analyze_migration.py` | Analyzes migration status and generates reports | `python3 scripts/data_migration/analyze_migration.py` |
| `clean_csv_files.py` | Cleans and standardizes CSV data files | `python3 scripts/data_migration/clean_csv_files.py` |

### 📁 `notion_processing/`
Scripts specifically for processing Notion exports and transforming them into the strategic system format.

| Script | Purpose | Usage |
|--------|---------|--------|
| `clean_notion_export.py` | Initial cleanup of Notion export files | `python3 scripts/notion_processing/clean_notion_export.py` |
| `analyze_notion_export.py` | Analyzes Notion export structure and content | `python3 scripts/notion_processing/analyze_notion_export.py` |
| `process_notion_files.py` | **Main processor** - cleans filenames, adds frontmatter, categorizes | `python3 scripts/notion_processing/process_notion_files.py` |
| `rename_notion_folders.py` | Batch renames Notion folder structures | `python3 scripts/notion_processing/rename_notion_folders.py` |
| `rename_notion_files.py` | Batch renames individual Notion files | `python3 scripts/notion_processing/rename_notion_files.py` |

### 📁 `screenshot_optimization/`
Complete screenshot quality management and optimization system.

| Script | Purpose | Usage |
|--------|---------|--------|
| `analyze_screenshots.py` | Analyzes screenshot quality and generates assessment | `python3 scripts/screenshot_optimization/analyze_screenshots.py` |
| `optimize_screenshots.py` | **Main optimizer** - crops, compresses, deletes poor quality | `python3 scripts/screenshot_optimization/optimize_screenshots.py` |
| `test_script_logic.py` | Validates screenshot processing logic without Pillow | `python3 scripts/screenshot_optimization/test_script_logic.py` |
| `cleanup_remaining_poor_quality.py` | Additional cleanup for missed poor-quality files | `python3 scripts/screenshot_optimization/cleanup_remaining_poor_quality.py` |

### 📁 `system_setup/`
System configuration, validation, and initial setup scripts.

| Script | Purpose | Usage |
|--------|---------|--------|
| `setup_dclt.py` | Initial DCLT system setup and configuration | `python3 scripts/system_setup/setup_dclt.py` |
| `quality_check.py` | System-wide quality validation and health checks | `python3 scripts/system_setup/quality_check.py` |

### 📁 Root `scripts/` Directory
Core strategic analysis and reporting tools (unchanged from original locations).

| Script | Purpose | Usage |
|--------|---------|--------|
| `strategic_query.py` | Strategic document querying and analysis | `python3 scripts/strategic_query.py` |
| `dashboard_generator.py` | Generates strategic planning dashboards | `python3 scripts/dashboard_generator.py` |
| `dependency_analyzer.py` | Analyzes project dependencies and conflicts | `python3 scripts/dependency_analyzer.py` |
| `resource_conflict_analyzer.py` | Identifies resource allocation conflicts | `python3 scripts/resource_conflict_analyzer.py` |
| `frontmatter_parser.py` | Parses and validates frontmatter across files | `python3 scripts/frontmatter_parser.py` |

## Usage Workflows

### 🚀 Complete System Setup (New Installation)
```bash
# 1. Initial system setup
python3 scripts/system_setup/setup_dclt.py

# 2. Process Notion export (if applicable)
python3 scripts/notion_processing/process_notion_files.py

# 3. Optimize screenshots (if applicable)  
python3 scripts/screenshot_optimization/optimize_screenshots.py

# 4. Run quality checks
python3 scripts/system_setup/quality_check.py

# 5. Generate strategic analysis
python3 scripts/dashboard_generator.py
```

### 📊 Notion Export Processing Workflow
```bash
# 1. Analyze export structure
python3 scripts/notion_processing/analyze_notion_export.py

# 2. Clean and process files
python3 scripts/notion_processing/process_notion_files.py

# 3. Validate migration
python3 scripts/data_migration/analyze_migration.py
```

### 🖼️ Screenshot Optimization Workflow
```bash
# 1. Analyze screenshot quality
python3 scripts/screenshot_optimization/analyze_screenshots.py

# 2. Run main optimization
python3 scripts/screenshot_optimization/optimize_screenshots.py

# 3. Additional cleanup if needed
python3 scripts/screenshot_optimization/cleanup_remaining_poor_quality.py
```

### 🔍 Strategic Analysis Workflow
```bash
# 1. Parse all frontmatter
python3 scripts/frontmatter_parser.py

# 2. Analyze dependencies
python3 scripts/dependency_analyzer.py

# 3. Check resource conflicts
python3 scripts/resource_conflict_analyzer.py

# 4. Generate dashboard
python3 scripts/dashboard_generator.py

# 5. Run strategic queries
python3 scripts/strategic_query.py
```

## Dependencies

### Python Packages
- **Pillow**: Required for screenshot optimization scripts
- **PyYAML**: Required for frontmatter processing
- **Pandas**: Required for data analysis scripts

### Installation
```bash
pip3 install --break-system-packages Pillow PyYAML pandas
```

## File Organization Benefits

### ✅ **Improved Discoverability**
- Logical grouping by function and purpose
- Clear naming conventions for related scripts
- Reduced root directory clutter

### ✅ **Better Maintenance**
- Related scripts grouped together
- Easier to update and modify related functionality
- Clear separation of concerns

### ✅ **Enhanced Workflow**
- Logical progression from setup → processing → analysis
- Clear entry points for different user needs
- Better documentation and usage examples

## Migration Notes

### **Previous Locations → New Locations:**
- Root directory scripts → `scripts/[category]/`
- All existing functionality preserved
- No breaking changes to script internals
- Updated paths in documentation

### **Backward Compatibility:**
Scripts can still be run from the project root using full paths:
```bash
# Still works
python3 scripts/screenshot_optimization/optimize_screenshots.py
```

## Next Steps

1. **Update any automation scripts** that reference old paths
2. **Review and test** scripts in new locations
3. **Consider creating shell aliases** for frequently used scripts
4. **Update CI/CD pipelines** if applicable

---

**Organization completed**: 2025-09-11  
**Scripts moved**: 13 files organized into 4 categories  
**Benefits**: Improved maintainability, discoverability, and workflow clarity