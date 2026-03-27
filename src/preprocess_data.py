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


def engineer_feats(main: pd.DataFrame) -> pd.DataFrame:

    for feat in feature_list:
        if "MORT" in feat:
            main["MORT_fac_rate"] = main["Count of Facility MORT Measures"] / main[feat].max()
            main["MORT_bet_rate"] = main["Count of MORT Measures Better"] / main["Count of Facility MORT Measures"]

        elif "Safety" in feat:
            main["Safety_fac_rate"] = main["Count of Facility Safety Measures"] / main[feat].max()
            main["Safety_bet_rate"] = main["Count of Safety Measures Better"] / main["Count of Facility Safety Measures"]

        elif "READM" in feat:
            main["READM_fac_rate"] = main["Count of Facility READM Measures"] / main[feat].max()
            main["READM_bet_rate"] = main["Count of READM Measures Better"] / main["Count of Facility READM Measures"]
        
        elif "Pt Exp" in feat:
            main["PtExp_fac_rate"] = main["Count of Facility Pt Exp Measures"] / main[feat].max()
                  
        elif "TE" in feat:
            main["TE_fac_rate"] = main["Count of Facility TE Measures"] / main[feat].max()
        
    return main


def main():
        
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean_data", required=True)
    ap.add_argument("--proc_data", required=True)
    args = ap.parse_args()

    raw_data = pd.read_parquet(args.clean_data)

    clean_data = engineer_feats(raw_data)

    # Write outputs to file
    output_path = Path(args.proc_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_data.to_parquet(output_path)    

    print("Written to file:", str(output_path))


if __name__ == "__main__":
    main()