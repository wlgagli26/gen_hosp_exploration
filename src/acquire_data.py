#Script for acquiring data and cleaning it

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd


feature_list = ['MORT Group Measure Count', 'Safety Group Measure Count', 'READM Group Measure Count',
           'Pt Exp Group Measure Count', 'TE Group Measure Count']
text_col = ['Facility Name', 'Address', 'City/Town', 'County/Parish']
num_col = ['Hospital overall rating', 'MORT Group Measure Count', 'Count of Facility MORT Measures', 
           'Count of MORT Measures Better', 'Count of MORT Measures No Different', 'Count of MORT Measures Worse',
           'Safety Group Measure Count', 'Count of Facility Safety Measures', 'Count of Safety Measures Better',
           'Count of Safety Measures No Different', 'Count of Safety Measures Worse', 'READM Group Measure Count',
           'Count of Facility READM Measures', 'Count of READM Measures Better', 'Count of READM Measures No Different',
           'Count of READM Measures Worse', 'Pt Exp Group Measure Count', 'Count of Facility Pt Exp Measures',
           'TE Group Measure Count', 'Count of Facility TE Measures']
id_col = ['Facility ID', 'Telephone Number']
cat_col = ['State', 'ZIP Code', 'Hospital Type', 'Hospital Ownership', 'Hospital overall rating footnote', 
           'MORT Group Footnote', 'Safety Group Footnote', 'READM Group Footnote', 'Pt Exp Group Footnote',
           'TE Group Footnote']
bool_col = ['Emergency Services', 'Meets criteria for birthing friendly designation']


def norm_text(c: pd.Series) -> pd.Series:
    """Normalize text in columns"""
    c = c.astype("string").str.strip().str.casefold()
    c = c.replace("", pd.NA)
    return c


def norm_num(c: pd.Series) -> pd.Series:
    """Normalize numeric columns to appropriate numbers"""
    c = pd.to_numeric(c, errors="coerce")
    return c


def norm_id(c: pd.Series) -> pd.Series:
    """Normalize id columnst to proper text"""
    c = c.astype("string").str.strip()
    c = c.replace("", pd.NA)
    return c


def norm_cat(c: pd.Series) -> pd.Series:
    """Normalize categorical columns into clean text"""
    c = c.astype("string").str.strip().str.casefold()
    c = c.replace("", pd.NA)
    return c


def norm_bool(c: pd.Series) -> pd.Series:
    """Normalize boolean columns into bool format"""
    c = c.astype("string").str.strip().str.casefold().isin(["yes", "y"])
    return c

'''
s = df["Meets criteria for birthing friendly designation"].astype("string").str.strip().str.casefold()

df["birth_friendly_yes"] = s.eq("yes")
df["birth_friendly_missing"] = s.isna() | s.eq("")
'''


def main():
        
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw_data", required=True)
    ap.add_argument("--output_data", required=True)
    args = ap.parse_args()

    raw_data = pd.read_excel(args.raw_data)

    for col in text_col:
        raw_data[col] = norm_text(raw_data[col])

    for col in num_col:
        raw_data[col] = norm_num(raw_data[col])

    for col in id_col:
        raw_data[col] = norm_id(raw_data[col])

    for col in cat_col:
        raw_data[col] = norm_cat(raw_data[col])    

    for col in bool_col:
        if col == "Meets criteria for birthing friendly designation":
            c = raw_data[col].astype("string").str.strip().str.casefold()
            c = c.replace("", pd.NA)
            raw_data["birth_friendly_YES"] = c.isin(["yes", "y"])
            raw_data["birth_friendly_MISSING"] = c.isna()
        else:
            raw_data[col] = norm_bool(raw_data[col])

   
    # Write outputs to file
    output_path = Path(args.output_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw_data.to_parquet(output_path)    

    print("Written to file:", str(output_path))


if __name__ == "__main__":
    main()