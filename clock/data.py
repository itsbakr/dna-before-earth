"""Load the CSV datasets in ``data/``. All analysis code reads data through here."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class Series:
    """A genome-size time series: one row per group."""

    name: str
    groups: list
    t: np.ndarray          # age, Gya
    y: np.ndarray          # log10 genome size, bp
    t_sd: np.ndarray       # assumed 1-sigma age uncertainty, Gyr
    y_sd: np.ndarray       # assumed 1-sigma log10 size uncertainty

    def subset(self, mask, name=None):
        mask = np.asarray(mask, bool)
        return Series(name or self.name, [g for g, m in zip(self.groups, mask) if m],
                      self.t[mask], self.y[mask], self.t_sd[mask], self.y_sd[mask])


def load_sharov(dates="figure"):
    """Sharov 2006 functional genome sizes.

    ``dates="figure"`` uses the ages Sharov plotted (eukaryotes 2.05, mammals 0.10), which reproduce
    his printed regression. ``dates="markov_reprint"`` uses Markov et al. 2010's reprint
    (eukaryotes 2.0, mammals 0.125).
    """
    df = pd.read_csv(DATA_DIR / "sharov_2006.csv")
    col = {"figure": "time_bya", "markov_reprint": "time_bya_markov_reprint"}[dates]
    return Series(f"Sharov 2006 ({dates} ages)", list(df.group), df[col].to_numpy(float),
                  np.log10(df.genome_bp.to_numpy(float)),
                  df.time_sd_assumed.to_numpy(float), df.log10_sd_assumed.to_numpy(float))


def load_node_ages():
    return pd.read_csv(DATA_DIR / "node_ages.csv")


def load_markov(dates="published"):
    """Markov et al. 2010 minimal genome sizes.

    ``dates="published"`` uses the ages in the paper. ``dates="current"`` replaces
    each age with the midpoint of the current estimate in ``node_ages.csv``
    (falling back to the published age where no current estimate exists).
    """
    df = pd.read_csv(DATA_DIR / "markov_2010.csv")
    t = df.time_bya.to_numpy(float)
    if dates == "current":
        t = current_ages(df.group)
    elif dates != "published":
        raise ValueError(f"unknown dates option: {dates}")
    return Series(f"Markov 2010 ({dates} ages)", list(df.group), t,
                  np.log10(df.mgs_mb.to_numpy(float) * 1e6),
                  df.time_sd_assumed.to_numpy(float), df.log10_sd_assumed.to_numpy(float))


def current_age_ranges(groups):
    """(low, high) current age range per group; published age when no estimate exists."""
    ages = load_node_ages().set_index("dataset_group")
    lo, hi = [], []
    for g in groups:
        row = ages.loc[g]
        if pd.isna(row.current_low_bya):
            lo.append(row.published_bya)
            hi.append(row.published_bya)
        else:
            lo.append(row.current_low_bya)
            hi.append(row.current_high_bya)
    return np.array(lo, float), np.array(hi, float)


def current_ages(groups):
    lo, hi = current_age_ranges(groups)
    return (lo + hi) / 2


def load_extended(include_only=True):
    df = pd.read_csv(DATA_DIR / "extended_dataset.csv")
    if include_only:
        df = df[df.include.astype(bool)]
    n = len(df)
    return Series("Extended (corrected)", list(df.group), df.time_bya.to_numpy(float),
                  np.log10(df.genome_mb.to_numpy(float) * 1e6),
                  np.full(n, np.nan), np.full(n, np.nan))
