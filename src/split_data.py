# Script for splitting data

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

target = ['Hospital overall rating']
count_list = ['MORT Group Measure Count', 'Safety Group Measure Count', 'READM Group Measure Count',
           'Pt Exp Group Measure Count', 'TE Group Measure Count']
text_col = ['Facility Name', 'Address', 'City/Town', 'County/Parish']
num_col = ['MORT Group Measure Count', 'Count of Facility MORT Measures', 
           'Count of MORT Measures Better', 'Count of MORT Measures No Different', 'Count of MORT Measures Worse',
           'Safety Group Measure Count', 'Count of Facility Safety Measures', 'Count of Safety Measures Better',
           'Count of Safety Measures No Different', 'Count of Safety Measures Worse', 'READM Group Measure Count',
           'Count of Facility READM Measures', 'Count of READM Measures Better', 'Count of READM Measures No Different',
           'Count of READM Measures Worse', 'Pt Exp Group Measure Count', 'Count of Facility Pt Exp Measures',
           'TE Group Measure Count', 'Count of Facility TE Measures']
id_col = ['Facility ID', 'Telephone Number']
cat_col = ['State', 'ZIP Code', 'Hospital Type', 'Hospital Ownership']  
drop_cols = ['MORT Group Footnote', 'Safety Group Footnote', 'READM Group Footnote', 'Pt Exp Group Footnote',
           'TE Group Footnote', 'Hospital overall rating footnote', 'Meets criteria for birthing friendly designation']
bool_col = ['Emergency Services',  'birth_friendly_YES', 'birth_friendly_MISSING']


def def_data(main: pd.DataFrame) -> pd.DataFrame:
    """Drop columns without signal or to reduce noise"""
    cols_to_drop = count_list + text_col + id_col + drop_cols
    new = main.drop(columns=cols_to_drop)
    return new

def split_data(main: pd.DataFrame) -> pd.DataFrame:
    """Split data into 80/20"""
    train_data, test_data = train_test_split(main, test_size=0.2, random_state=75)
    return train_data, test_data


def sep_label(main: pd.DataFrame) -> pd.DataFrame:
    """Separate label from features"""
    X = main.drop(columns=target)
    y = main[target]
    return X, y



def main():
        
    ap = argparse.ArgumentParser()
    ap.add_argument("--get_data", required=True)
    ap.add_argument("--output_train", required=True)
    ap.add_argument("--output_test", required=True)
    args = ap.parse_args()

    final_data = pd.read_parquet(args.get_data)

    final_data = def_data(final_data)
    train_data, test_data = split_data(final_data)
    X_train, y_train = sep_label(train_data)
    X_test, y_test = sep_label(test_data)
   
    # Write outputs to file
    output_path_tr = Path(args.output_train)
    output_path_tr.parent.mkdir(parents=True, exist_ok=True)
    output_path_te = Path(args.output_test)
    output_path_te.parent.mkdir(parents=True, exist_ok=True)
    train_data.to_parquet(output_path_tr)    
    test_data.to_parquet(output_path_te)   

    print("Train data written to file:", str(output_path_tr))
    print("Test data written to file:", str(output_path_te))


if __name__ == "__main__":
    main()