#Script for modeling data

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import joblib
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import (mean_absolute_error, root_mean_squared_error, r2_score)


target = 'Hospital overall rating'

def load_preds(path: str) -> pd.DataFrame:
    """load predictions from parquet"""
    preds = pd.read_parquet(path)[['Hospital overall rating', 'predicted']]
    return preds

def eval_model(preds: pd.DataFrame, model_name: str) -> Dict[str: Any]:
    model = preds[[target, 'predicted']].dropna().copy()
    y_true, y_pred = model[target], model['predicted']
    rmse = root_mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f'{model_name} Model\nRMSE: {rmse}\nMAE: {mae}\nR2: {r2}\n')
    metrics_dict = {model_name: {"RMSE": rmse,
                                 "MAE": mae,
                                 "R2 Score": r2}
    }
    return metrics_dict
    

def main():
        
    ap = argparse.ArgumentParser()
    ap.add_argument("--rf_preds", required=True)
    ap.add_argument("--xgb_preds", required=True)
    ap.add_argument("--metrics_out", required=True)

    args = ap.parse_args()

    rf_metrics = eval_model(load_preds(args.rf_preds), 'RF')
    xgb_metrics = eval_model(load_preds(args.xgb_preds), 'XGB')

    metrics_dict = rf_metrics | xgb_metrics

   
    # Write outputs to file

    Path(args.metrics_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.metrics_out).write_text(json.dumps(metrics_dict, indent=2))
    
    print("Written to metrics file.")


if __name__ == "__main__":
    main()