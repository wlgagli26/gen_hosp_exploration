#Script for modeling data

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import joblib
from typing import Dict, Tuple
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import numpy as np
import pandas as pd

target = 'Hospital overall rating'
model_list = ['XGB', 'RF']

def sep_label(main: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Separate label from features"""
    X = main.drop(columns=target)
    y = pd.to_numeric(main[target], errors='coerce')
    return X, y

def xgb_model(
        train: pd.DataFrame, 
        test: pd.DataFrame,
        xgb_args: dict[str, Any] | None = None
        ) -> Tuple[pd.DataFrame, XGBRegressor]:
    
    xgb_args = xgb_args or {}
    train = train.dropna(subset=[target]).copy()
    print("train target nulls:", train[target].isna().sum())
    print("test target nulls:", test[target].isna().sum() if target in test.columns else "target not in test")

    X_train, y_train = sep_label(train)
    X_test, y_test = sep_label(test)

    X_train = pd.get_dummies(X_train, drop_first=False)
    X_test = pd.get_dummies(X_test, drop_first=False)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)
    #y_train = y_train - 1  #for classificaiton
    
    xgb = XGBRegressor(**xgb_args)
    xgb.fit(X_train, y_train)
    preds = xgb.predict(X_test) #+ 1  #use to fix after reordering from classification

    eval_matrix = test.copy()
    eval_matrix["predicted"] = preds

    return eval_matrix, xgb


def rf_model(
        train: pd.DataFrame, 
        test: pd.DataFrame,
        rf_args: dict[str, Any] | None = None
        ) -> Tuple[pd.DataFrame, RandomForestRegressor]:
    
    rf_args = rf_args or {}
    train = train.dropna(subset=[target]).copy()
    print("train target nulls:", train[target].isna().sum())
    print("test target nulls:", test[target].isna().sum() if target in test.columns else "target not in test")

    X_train, y_train = sep_label(train)
    X_test, y_test = sep_label(test)

    X_train = pd.get_dummies(X_train, drop_first=False)
    X_test = pd.get_dummies(X_test, drop_first=False)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)
    
    rf = RandomForestRegressor(**rf_args)
    rf.fit(X_train, y_train)
    preds = rf.predict(X_test)

    eval_matrix = test.copy()
    eval_matrix["predicted"] = preds
    

    return eval_matrix, rf
         


def main():
        
    ap = argparse.ArgumentParser()
    ap.add_argument("--select_model", required=True, choices=['rf', 'xgb'])
    ap.add_argument("--train_data", required=True)
    ap.add_argument("--test_data", required=True)

    
    ap.add_argument("--models", required=True)
    ap.add_argument("--preds", required=True)
    ap.add_argument("--best_params", default=None)
    ap.add_argument("--random_seed", type=int, default=75)

    # Random Forest tuning parameters
    ap.add_argument("--rf_n_estimators", type=int, default=200)
    ap.add_argument("--rf_max_depth", type=int, default=7)
    ap.add_argument("--rf_min_samples_leaf", type=int, default=8)

    # XGBoost tuning parameters
    ap.add_argument("--xgb_n_estimators", type=int, default=200)
    ap.add_argument("--xgb_max_depth", type=int, default=7)
    ap.add_argument("--xgb_learning_rate", type=float, default=0.05)
    ap.add_argument("--xgb_subsample", type=float, default=0.8)
    ap.add_argument("--xgb_colsample_bytree", type=float, default=0.8)
    
    args = ap.parse_args()

    tuned_params = {}
    if args.best_params:
        tuned_params = json.loads(Path(args.best_params).read_text())

    train_data = pd.read_parquet(args.train_data)
    test_data = pd.read_parquet(args.test_data)


    if args.select_model == "rf":
        
        rf_params = {
            "n_estimators": tuned_params.get("n_estimators", args.rf_n_estimators),
            "max_depth": tuned_params.get("max_depth", args.rf_max_depth),
            "min_samples_leaf": tuned_params.get("min_samples_leaf", args.rf_min_samples_leaf),
            "random_state": tuned_params.get("random_state", args.random_seed)
        }

        preds_df, model = rf_model(train_data, test_data, rf_params)
    
    elif args.select_model == "xgb":
        xgb_params = {
            "n_estimators": tuned_params.get("n_estimators", args.xgb_n_estimators),
            "max_depth": tuned_params.get("max_depth", args.xgb_max_depth),
            "learning_rate": tuned_params.get("learning_rate", args.xgb_learning_rate),
            "subsample": tuned_params.get("subsample", args.xgb_subsample),
            "colsample_bytree": tuned_params.get("colsample_bytree", args.xgb_colsample_bytree),
            "random_state": tuned_params.get("random_state", args.random_seed)
        }

        preds_df, model = xgb_model(train_data, test_data, xgb_params)



    # Write outputs to file
    
    Path(args.models).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.models)
    
    output_path = Path(args.preds)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    preds_df.to_parquet(output_path)    

    print("Written to file:", str(output_path))


if __name__ == "__main__":
    main()