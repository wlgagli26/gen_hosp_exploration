# General Hospital Exploration Using Version Control

## Purpose

The purpose of this project is to create a version-controlled repository for exploration of the General Hospital Information from CMS regarding Care Compare on Medicare.gov. 


## Data Source


## Reproducible Workflow

Using dvc and uv for dependencies, this project creates the following reproducible **DVC workflow stages**:

#### Data Acquisition and Cleaning:

`data_acquisition`

The dataset is pulled into the variable space for future use. The dataset is then cleaned to ensure all data are in a consistent and usable format for analysis.

*inputs*:
    -`data/Hospital_General_Info.xlsx`

*outputs*:
    -`data/data_clean.parquet`



#### Feature Engineering:

`process_data`

The cleaned dataset is further processed to explore engineered features derived from the original data for analysis.

*inputs*:
    -`data/data_clean.parquet`

*outputs*
    -`data/processed/data_final.parquet`

