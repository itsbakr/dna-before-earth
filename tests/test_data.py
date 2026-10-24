import numpy as np

from clock import data


def test_sharov_matches_published_table():
    s = data.load_sharov()
    assert s.groups == ["Prokaryotes", "Eukaryotes", "Worms", "Fish", "Mammals"]
    np.testing.assert_allclose(s.t, [3.5, 2.0, 1.0, 0.5, 0.125])
    np.testing.assert_allclose(10 ** s.y / 1e6, [0.5, 2.9, 72.8, 133.3, 480])


def test_markov_ages_are_nested_and_decreasing():
    for dates in ("published", "current"):
        m = data.load_markov(dates)
        assert len(m.t) == 9
        assert np.all(np.diff(m.t) < 0), dates


def test_current_age_ranges_are_ordered():
    lo, hi = data.current_age_ranges(data.load_markov().groups)
    assert np.all(lo <= hi)


def test_extended_has_no_duplicate_genomes_among_included_rows():
    import pandas as pd
    df = pd.read_csv(data.DATA_DIR / "extended_dataset.csv")
    inc = df[df.include.astype(bool)]
    assert not inc.species.duplicated().any()
    assert len(data.load_extended().t) == len(inc)
