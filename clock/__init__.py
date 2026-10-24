"""Tools for testing the genome-complexity clock hypothesis.

Conventions used throughout the package:

* ``t`` is age in billions of years before present (Gya), positive into the past.
* ``y`` is log10 of genome size in base pairs.
* A straight-line clock is ``y = a - b * t``, so ``b`` is the growth rate in
  log10 units per billion years and the age at which the line reaches ``y0``
  is ``(a - y0) / b``.
"""
