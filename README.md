# General Hospital Exploration Using Version Control
*By Virginia Muthard*

## Purpose

The purpose of this project is to create a version-controlled repository for exploration of the General Hospital Information from CMS regarding Care Compare on Medicare.gov. It is a work-in-progress for building out and applying tasks related to the implementation of various data science skills.


## Data Source


## Reproducible Workflow

Using dvc and uv for dependencies, this project creates the following reproducible **DVC workflow stages**:

---

#### Data Acquisition and Cleaning:

`data_acquisition`

The dataset is pulled into the variable space for future use. The dataset is then cleaned and some features engineered 
to ensure all data are in a consistent and usable format for analysis.

*inputs*:
- `data/Hospital_General_Info.xlsx`

*outputs*:
- `data/data_clean.parquet`  
  
<br>
  
`preprocess_data`

*inputs*:
- `data/processed/data_clean.parquet`
      
*outputs*
- `data/processed/data_final.parquet`
    
---

#### Exploratory Data Analysis:

The data is explored for distributions and trends to give insights into data splitting and modeling approaches as appropriate.

`eda_notebook`

*inputs*:
- `data/processed/data_final.parquet`
- `data/raw/Hospital_General_Info.xlsx`
    
*outputs*:
- `reports/eda_report.ipynb`  
  
---  
  
#### Data Splitting:

The data is split in preparation for analysis and output to separate train/test files for ease of modeling and reproducibility.

`split_data`

*inputs*:
- `data/processed/data_final.parquet`

*outputs*:
- `data/processed/train_data.parquet`
- `data/processed/test_data.parquet`
