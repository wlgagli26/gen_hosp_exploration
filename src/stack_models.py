# Stack models to try to boost results--COME BACK TO THIS TO EDIT

import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor


def make_oof_pred(
    X: pd.DataFrame,
    y: pd.Series,
    model,
    n_splits: int = 5,
    random_seed: int = 75,
) -> tuple[np.ndarray, list]:
    cv = KFold(n_splits=n_splits, shuffle=True, random_state=random_seed)
    oof_pred = np.zeros(len(X))
    fitted_models = []

    for train_idx, valid_idx in cv.split(X, y):
        X_tr = X.iloc[train_idx]
        y_tr = y.iloc[train_idx]
        X_va = X.iloc[valid_idx]

        m = clone(model)
        m.fit(X_tr, y_tr)
        oof_pred[valid_idx] = m.predict(X_va)
        fitted_models.append(m)

    return oof_pred, fitted_models