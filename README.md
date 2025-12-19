# ArcGIS Feature Layer Updater

Automated pipeline for transforming tabular data from Google Spreadsheets and updating a hosted **ArcGIS Online Feature Layer** using **ArcGIS API for Python**.

This project was implemented as a solution for the *GIS Developer* technical task and focuses on **full automation**, minimal manual interaction, and clear data mapping between tabular and spatial data.

---

## Overview

The solution consists of two logical stages:

1. **Data preparation**
   - Load source data from Google Spreadsheets
   - Normalize and expand rows based on value counts (`Значення 1` – `Значення 10`)
   - Convert coordinates to numeric format
   - Export the transformed dataset to CSV

2. **Feature Layer update**
   - Connect to ArcGIS Online
   - Clear existing features in the hosted Feature Layer
   - Upload new point features with attributes and geometry
   - Ensure attribute mapping aligns with the layer schema

All steps are executed automatically via Python scripts.

---

## Environment Variables
Use command ```cp .env.example .env``` 

### Environment variables in .env.example:
GIS_USERNAME=your_arcgis_username 

GIS_PASSWORD=your_arcgis_password 

ITEM_ID=815e5b14c4da48109f941d1560b75395 

CSV_FILE_NAME=prepared_data.csv

GIS_URL=https://www.arcgis.com

---

## Running with Docker (Recommended)

The entire pipeline can be executed using Docker Compose:
```docker-compose up```

At the end of the execution the script will show:
```INFO:__main__:Features updated successfully.```

Otherwise, error code will be shown

This ensures:

- Consistent execution environment

- No manual dependency installation

- Fully automated workflow

Data Processing Logic
----------------------

For each row in the source spreadsheet:

• If any of **Значення 1 – Значення 10** > 0  
• The row is expanded into **N rows**, where **N** equals the maximum value across those columns  
• Each expanded row contains:
  - Duplicated metadata (date, region, city, coordinates)
  - Binary indicators (**1** or **0**) for each value column

This logic follows the task specification exactly.

Feature Layer Mapping
-----------------------

| Feature Layer Field | Source Column |
|---------------------|---------------|
| date_1              | Дата          |
| Область             | Область       |
| city                | Місто         |
| value_1             | Значення 1    |
| ...                 | ...           |
| value_10            | Значення 10   |
| long                | long          |
| lat                 | lat           |

Geometry is created as **Point (WGS84 / EPSG:4326)** using `long` and `lat`.

Feature Update Strategy
-------------------------

The update process is fully automated:

• Query existing features (`where="1=1"`)  
• Delete all existing records  
• Add newly prepared features via `edit_features(adds=...)`

This ensures the layer always reflects the latest spreadsheet state.

Technologies Used
-------------------

- Python 3.10+  
- Pandas  
- dotenv
- ArcGIS API for Python
- Docker / Docker Compose  

Expected Result
-----------------

• Points displayed on the ArcGIS Online map  
• Each point contains a popup with prepared attribute values  
• No manual operations in ArcGIS UI required  

Notes
-------

- Column names are mapped according to feature layer but not test task, in order to map data correctly
- Updated data is stored in local file called prepared_data.csv
- Additionally, updated data is stored with already mapped columns for simplicity
- Credentials are handled via environment variables  
- HTTPS warnings may appear if SSL verification is disabled (safe for test environment)  
- Script is idempotent — running it multiple times produces consistent results
- Used pandas to focus on the core transformation logic first, because it allowed faster iteration and clearer implementation of the required row-expansion rules. In a production version, I would replace the Excel input with Google Sheets API to fully automate data retrieval and avoid manual exports.

# If there's a need for future code modifications
Please write to me via email: ```contact.roman.sapun@gmail.com```
