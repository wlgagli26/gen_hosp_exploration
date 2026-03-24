#Script for processing data in prep for EDA

from __future__ import annotations

import argparse
import json
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from pathlib import Path


def engineer_feats(c: pd.Series) -> pd.Series:
    
