"""Autocorrelation, decorrelation timescale, and cross-correlation.

Worked helpers: :func:`autocorr`, :func:`integral_timescale`, :func:`effective_dof`.
Student stub: :func:`cross_correlation`.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import signal, stats


def autocorr(x: ArrayLike, biased: bool = True) -> NDArray[np.float64]:
    """One-sided sample autocorrelation ``R(tau)`` with ``R(0) = 1``.

    Notes
    -----
    The biased and unbiased estimates agree at small lag (many pairs) and diverge
    at large lag; the biased tail is damped toward zero while the unbiased tail
    fans out. See the lecture figure comparing white noise, AR(1), and a sinusoid.
    """
    d = np.asarray(x, dtype=float)
    d = d[np.isfinite(d)]
    d = d - d.mean()
    n = d.size
    var = d.var()
    full = np.correlate(d, d, "full")[n - 1 :]  # lags 0 .. n-1
    if biased:
        return full / (n * var)
    return full / ((n - np.arange(n)) * var)


def integral_timescale(x: ArrayLike, dt: float, biased: bool = True) -> float:
    """Integral (decorrelation) timescale ``T*`` by trapezoid to the first zero."""
    R = autocorr(x, biased=biased)
    tau = 0.0
    i = 0
    while i + 1 < len(R) and R[i] >= 0:
        tau += dt * (R[i] + R[i + 1]) / 2.0
        i += 1
    return tau


def effective_dof(x: ArrayLike, dt: float, biased: bool = True) -> float:
    """Effective (equivalent) degrees of freedom ``EDOF`` for a series."""
    # t_int = integral_timescale(x, dt, biased=biased)
    # record = N * dt  (N = number of finite samples)
    # EDOF = record / (2 * T*)   -- the factor of 2 is DOF -> EDOF

    d = np.asarray(x, dtype=float)
    d = d[np.isfinite(d)]
    n = d.size
    t_int = integral_timescale(d, dt=dt, biased=biased)
    record = n * dt
    # EDOF = DOF / 2 = record / (2 T*)
    edof = record / (2.0 * t_int)
    return float(edof)


def cross_correlation(
    x: ArrayLike, y: ArrayLike
) -> tuple[NDArray[np.int_], NDArray[np.float64]]:
    """Normalised cross-correlation of two series, with the lag axis.
    Notes:
    Sign convention: the peak sits at the lag by which ``y`` is shifted relative
    to ``x``. If ``y`` lags ``x`` by ``k`` samples (``x`` leads) the peak is at
    ``-k``; so a **negative** peak lag means ``x`` leads ``y``, a positive one
    means ``y`` leads ``x``."""

    # I'll set 26°N as x, then tau < 0 means 26°N leads 47°N → positive lag。
    arr_x = np.asarray(x, dtype=float)
    arr_y = np.asarray(y, dtype=float)

    # filter invalid data points
    mask = np.isfinite(arr_x) & np.isfinite(arr_y)
    x_clean = arr_x[mask]
    y_clean = arr_y[mask]
    n = x_clean.size

    # std, move the center&average of array to 0., and zoom in the amplitude to 1. Then r ∈ 【-1， 1】.
    xa = (x_clean - np.mean(x_clean)) / np.std(x_clean)
    ya = (y_clean - np.mean(y_clean)) / np.std(y_clean)

    # cross-correlate
    r = signal.correlate(xa, ya, mode="full") / n
    lags = signal.correlation_lags(n, n, mode="full")

    return lags, r


def cross_correlation_significance(
    x: ArrayLike,
    y: ArrayLike,
    r_val: float,
    dt: float = 1.0,
    alpha: float = 0.05,
) -> dict[str, float | bool]:
    """ssess statistical significance of a cross-correlation peak after autocorrelation."""
    arr_x = np.asarray(x, dtype=float)
    arr_y = np.asarray(y, dtype=float)

    # N_eff
    n_eff = float(min(effective_dof(arr_x, dt=dt), effective_dof(arr_y, dt=dt)))

    df = n_eff - 2
    if df <= 0:
        return {"n_eff": n_eff, "r_crit": 1.0, "significant": False}

    t_crit = stats.t.ppf(1 - alpha / 2, df)
    r_crit = np.sqrt(t_crit**2 / (t_crit**2 + df))

    return {
        "n_eff": n_eff,
        "r_crit": float(r_crit),
        "significant": bool(abs(r_val) > r_crit),
    }
