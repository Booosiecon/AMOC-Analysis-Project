from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import xarray as xr
from numpy.typing import ArrayLike

# from typing import Any


def plot_umo_comparison(
    time: ArrayLike,
    calculated_umo: ArrayLike,
    official_umo: ArrayLike,
    figsize: tuple[float, float] = (15, 5),
    dpi: int = 600,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot overlay comparison of claculated and offical UMO transport series."""

    t = np.asarray(time)
    calc = np.asarray(calculated_umo, float)
    official = np.asarray(official_umo, float)

    fig, ax = plt.subplots(figsize = figsize)

    ax.plot(
        t,
        calc,
        label = "Calculated UMO Transport",
        color = "tab:blue",
        alpha = 0.8,
        linewidth = 1.0,
    )

    ax.plot(
        t,
        official,
        label = "offical UMO transport",
        color = "tab:grey",
        alpha = 0.8,
        linewidth = 1.0,
    )

    ax.set_xlabel("Time", fontsize = 16)
    ax.set_ylabel("Transport (Sv)", fontsize = 16)
    ax.set_title(
        "Comparison of Calculated and Official UMO Transport Series",
        fontsize = 18,
        fontweight = "bold",
    )

    ax.margins(x = 0.01)  # leave a 1% margin
    ax.set_ylim(-40, 10)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

    ax.tick_params(axis = "both", which = "major", labelsize = 14)

    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc = "lower left", frameon = True, fontsize = 14)

    fig.tight_layout()
    return fig, ax


def plot_series_scatter_and_regression(
    results: dict[str, float | int | np.ndarray],
    name_x: str = "Calculated UMO Transport (Sv)",
    name_y: str = "Official UMO Transport (Sv)",
    title: str = "Regression Analysis",
    figsize: tuple[float, float] = (6.5, 6),
    dpi: int = 600,
) -> tuple[plt.Figure, plt.Axes]:
    """Make a scatter plot and linear regression with 1:1 reference line and statistical summary."""
    x = np.asarray(results["x"])
    y = np.asarray(results["y"])
    slope = float(results["slope"])
    intercept = float(results["intercept"])

    fig, ax = plt.subplots(figsize = figsize, dpi = dpi)

    # scatter plot
    ax.scatter(
        x,
        y,
        color = "tab:blue",
        alpha = 0.35,
        s = 12,
        edgecolors = "none",
        label = "Data points",
    )

    # linear regression
    x_grid = np.linspace(x.min(), x.max(), 100)
    y_fit = slope * x_grid + intercept
    ax.plot(
        x_grid,
        y_fit,
        color = "tab:red",
        linewidth = 1.0,
        label = f"Fit: $y = {slope:.3f}x {intercept:+.3f}$",
    )

    # 1:1 reference line
    lim_min = min(x.min(), y.min())
    lim_max = max(x.max(), y.max())
    ax.plot(
        [lim_min, lim_max],
        [lim_min, lim_max],
        color = "gray",
        linestyle = "--",
        linewidth = 1.2,
        alpha = 0.7,
        label = "1:1 Reference",
    )

    # comment box
    p_val = float(results["p-value"])
    if p_val < 1e-4:
        p_str = "$p < 10^{-4}$"
    else:
        p_str = f"$p = {p_val:.4e}$"

    stats_text = (
        f"$N$ = {results['n_samples']:,}\n"
        f"$r$ = {results['r']:.3f} ({p_str})\n"
        f"$R^2$ = {results['r2']:+.3f} \n"
        f"Mean Bias = {results['bias']:+.3f} Sv\n"
        f"Root Mean Square Error = {results['rmse']:.3f} Sv \n"
        f"Slope Standard Error = {results['stderror']:.3f}"
    )

    ax.text(
        0.05,
        0.95,
        stats_text,
        transform = ax.transAxes,
        fontsize = 9.5,
        verticalalignment = "top",
        bbox=dict(
            boxstyle = "round,pad=0.4",
            facecolor = "white",
            alpha = 0.5,
            edgecolor = "gray",
        ),
    )

    ax.set_xlabel(name_x, fontsize = 16)
    ax.set_ylabel(name_y, fontsize = 16)
    ax.set_title(title, fontsize = 18, fontweight = "bold")
    ax.grid(True, linestyle = "--", alpha = 0.5)
    ax.legend(loc = "best", frameon = True, fontsize = 10)

    fig.tight_layout()
    return fig, ax


def plot_monthly_climatology(
    clim_moc: xr.DataArray,
    clim_umo: xr.DataArray,
    figsize: tuple[float, float] = (15, 5),
    dpi: int = 600,
) -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]:
    """Plot monthly climatology of MOC and TRANS_UMO."""

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize = figsize, dpi = dpi, sharex = True
    )  # 2 subplots share the same x-axis
    months = range(1, 13)

    # MOC seasonal cycle
    ax1.plot(
        clim_moc["month"], clim_moc.values, marker = "o", color = "tab:red", linewidth = 2
    )
    ax1.set_title("MOC Monthly Climatology (26°N)", fontsize = 16, fontweight = "bold")
    ax1.set_xlabel("Month", fontsize=16)
    ax1.set_ylabel("Transport (Sv)", fontsize = 16)
    ax1.set_xticks(months)
    ax1.grid(True, linestyle = "--", alpha = 0.5)

    # UMO seasonal cycle
    ax2.plot(
        clim_umo["month"], clim_umo.values, marker = "o", color = "tab:blue", linewidth = 2
    )
    ax2.set_title("UMO Monthly Climatology (26°N)", fontsize = 16, fontweight = "bold")
    ax2.set_xlabel("Month", fontsize = 16)
    ax2.set_ylabel("Transport (Sv)", fontsize = 16)
    ax2.set_xticks(months)
    ax2.grid(True, linestyle = "--", alpha = 0.5)

    fig.tight_layout()
    return fig, (ax1, ax2)


def plot_raw_vs_deseasonalised(
    time: ArrayLike,
    da_moc: xr.DataArray,
    deseason_moc: xr.DataArray,
    da_umo: xr.DataArray,
    deseason_umo: xr.DataArray,
    figsize: tuple[float, float] = (15, 8),
    dpi: int = 600,
) -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]:
    """Plot raw series with thicker/darker deseasonalised series overlaid"""

    t = np.asarray(time)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = figsize, dpi = dpi, sharex = True)

    # MOC comparison
    ax1.plot(
        t, da_moc.values, color = "salmon", alpha = 0.8, linewidth = 1.0, label = "Raw MOC"
    )
    ax1.plot(
        t,
        deseason_moc.values,
        color = "darkred",
        linewidth = 1.5,
        label = "Deseasonalised MOC (Mean kept)",
    )
    ax1.set_ylabel("Transport (Sv)", fontsize = 16)
    ax1.set_title(
        "MOC Raw and Deseasonalised Series (26°N)", fontsize = 18, fontweight = "bold"
    )
    ax1.grid(True, linestyle = "--", alpha = 0.5)
    ax1.legend(loc = "best", fontsize = 14, framealpha = 0.0)

    # UMO comparison
    ax2.plot(
        t, da_umo.values, color = "skyblue", alpha = 0.8, linewidth = 1.0, label = "Raw UMO"
    )
    ax2.plot(
        t,
        deseason_umo.values,
        color = "navy",
        linewidth = 1.5,
        label = "Deseasonalised UMO (Mean kept)",
    )
    ax2.set_xlabel("Time", fontsize = 16)
    ax2.set_ylabel("Transport (Sv)", fontsize = 16)
    ax2.set_ylim(-32, -5)
    ax2.set_title(
        "UMO Raw and Deseasonalised Series (26°N)", fontsize = 18, fontweight = "bold"
    )
    ax2.grid(True, linestyle = "--", alpha = 0.5)
    ax2.legend(loc = "best", fontsize = 14, framealpha = 0.0)

    fig.tight_layout()
    return fig, (ax1, ax2)


def plot_autocorrelation(
    lags: ArrayLike,
    r: ArrayLike,
    t_int: float,
    var_name: str,
    color: str,
    max_lag: float,
    figsize: tuple[float, float] = (8, 4),
    dpi: int = 600,
) -> tuple[plt.Figure, plt.Axes]:
    """PLot autocorrelation with T*"""
    lags = np.asarray(lags, dtype = float)
    r = np.asarray(r, dtype = float)

    # mask = lags <= max_lag
    # lags_plot = lags[mask]
    # r_plot = r[mask]

    fig, ax = plt.subplots(figsize = figsize, dpi = dpi)

    ax.plot(
        lags,
        r,
        color = color,
        linewidth = 1.5,
        label = f"{var_name} Autocorrelation $R(\\tau)$",
    )
    ax.axhline(0, color = "gray", linestyle = "-", linewidth = 0.8, alpha = 0.8)

    ax.axvline(
        x = t_int,
        color = "black",
        linestyle = "--",
        linewidth = 1.5,
        label=f"$T^{{*}} = {t_int:.2f}$ days",
    )

    ax.set_title(
        f"{var_name} Autocorrelation with $T^*$", fontsize = 16, fontweight = "bold"
    )
    ax.set_xlabel("Lag $\\tau$ (day)", fontsize = 14)
    ax.set_ylabel("Autocorrelation $R(\\tau)$", fontsize = 14, fontweight = "bold")
    ax.set_xlim(0, max_lag)
    ax.set_ylim(-0.4, 1.05)
    ax.grid(True, linestyle = "--", alpha = 0.5)
    ax.legend(loc = "best", frameon = True, fontsize = 14)

    fig.tight_layout()
    return fig, ax


def plot_matched_series_comparison(
    time_raw1: ArrayLike,
    x_raw1: ArrayLike,
    time_raw2: ArrayLike,
    x_raw2: ArrayLike,
    time_m1: ArrayLike,
    x_m1: ArrayLike,
    time_m2: ArrayLike,
    x_m2: ArrayLike,
    name1: str = "Series 1",
    name2: str = "Series 2",
    figsize: tuple[float, float] = (14, 7),
    dpi: int = 600,
) -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]:
    """Before/after figure of the matched 2 series."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = figsize, dpi = dpi, sharex = True)

    # before
    ax1.plot(
        time_raw1, x_raw1, color = "tab:blue", alpha = 0.8, lw = 1.0, label = f"Raw {name1}"
    )
    ax1.plot(
        time_raw2, x_raw2, color = "tab:red", alpha = 0.8, lw = 1.0, label = f"Raw {name2}"
    )
    ax1.set_ylabel("Transport (Sv)", fontsize = 16)
    ax1.set_title("Before Matching", fontsize = 18, fontweight = "bold")
    ax1.grid(True, linestyle = "--", alpha = 0.5)
    ax1.legend(loc = "upper left", frameon = True, fontsize = 16)

    # after
    ax2.plot(
        time_m1,
        x_m1,
        color = "tab:blue",
        alpha = 0.8,
        lw = 1.5,
        marker = "o",
        markersize = 2,
        label = f"Matched {name1}",
    )
    ax2.plot(
        time_m2,
        x_m2,
        color = "tab:red",
        alpha = 0.8,
        lw = 1.5,
        marker = "o",
        markersize = 2,
        label = f"Matched {name2}",
    )
    ax2.set_xlabel("Time", fontsize = 16)
    ax2.set_ylabel("Transport (Sv)", fontsize = 16)
    ax2.set_title("After Matching", fontsize = 18, fontweight = "bold")
    ax2.grid(True, linestyle = "--", alpha = 0.5)
    ax2.legend(loc = "lower left", frameon = True, fontsize = 16)

    fig.tight_layout()
    return fig, (ax1, ax2)



def plot_cross_relation_comparison(
    lags: ArrayLike,
    r_raw: ArrayLike,
    r_deseason: ArrayLike,
    peak_raw: tuple[float, float] | None = None,
    peak_deseason: tuple[float, float] | None = None,
    var_names: tuple[str, str] = ("26°N MOC", "47°N MOC"),
    figsize: tuple[float, float] = (10, 5),
    dpi: int = 600,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot cross-correlation raw and deseasonalised."""
    lags = np.asarray(lags, dtype=float)
    r_raw = np.asarray(r_raw, dtype=float)
    r_deseason = np.asarray(r_deseason, dtype=float)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # curves
    ax.plot(
        lags,
        r_raw,
        color = "tab:gray",
        linestyle = "--",
        linewidth = 1.5,
        label = "Raw Series Cross-Correlation",
    )
    ax.plot(
        lags,
        r_deseason,
        color = "tab:red",
        linewidth = 2.0,
        label = "Deseasonalised Series Cross-Correlation",
    )

    # mark peak
    ax.scatter(
        [peak_raw[0]], [peak_raw[1]], color = "gray", s = 50, zorder = 5, edgecolor = "black"
    )
    ax.scatter(
        [peak_deseason[0]],
        [peak_deseason[1]],
        color = "tab:red",
        s = 60,
        zorder = 5,
        edgecolor = "black",
    )

    ax.axhline(0, color = "black", linestyle = "-", linewidth = 0.8, alpha = 0.7)
    ax.axvline(0, color = "gray", linestyle = ":", linewidth = 1.0, alpha = 0.7)

    # comment box
    text_str = (
        f"• Raw lag = {int(peak_raw[0])}mon, r = {peak_raw[1]:.2f}\n"
        f"• Deseasonalised lag = {int(peak_deseason[0])}mon, r = {peak_deseason[1]:.2f}"
    )
    props = dict(boxstyle = "round", facecolor = "white", alpha = 0.8, edgecolor = "gray")
    ax.text(
        0.98,
        0.95,
        text_str,
        transform = ax.transAxes,
        fontsize = 11,
        verticalalignment = "top",
        horizontalalignment = "right",
        multialignment = "left",
        bbox=props,
    )

    ax.set_title(
        f"Cross-Correlation\n {var_names[0]} and {var_names[1]}",
        fontsize = 16,
        fontweight = "bold",
    )
    ax.set_xlabel("Lag $\\tau$ (month) (Positive $\\to$ 47° leads 26°)", fontsize = 14)
    ax.set_ylabel("Normalised Cross-Correlation $r$", fontsize = 14)
    ax.grid(True, linestyle="--", alpha = 0.5)
    ax.legend(loc = "best", frameon = True, fontsize = 12)

    fig.tight_layout()
    return fig, ax


def plot_lagged_scatter(
    x_series: ArrayLike,
    y_series: ArrayLike,
    peak_lag: int,
    var_names: tuple[str, str] = ("26°N", "47°N"),
    figsize: tuple[float, float] = (6, 6),
    dpi: int = 600,
    ax: plt.Axes | None = None,
    title_suffix: str = "",
) -> tuple[plt.Figure, plt.Axes]:
    """Scatter at the peak lag"""

    x = np.asarray(x_series, float)
    y = np.asarray(y_series, float)

    # if peak_lag > 0 (y leads x), remove the last 32 months of x and the beginning 32 months of y
    if peak_lag > 0:
        x_aligned = x[:-peak_lag]
        y_aligned = y[peak_lag:]
    elif peak_lag < 0:
        x_aligned = x[-peak_lag:]
        y_aligned = y[:peak_lag]
    else:
        x_aligned = x
        y_aligned = y

    # linear fit for the scatter
    slope, intercept = np.polyfit(x_aligned, y_aligned, 1)
    r_val = np.corrcoef(x_aligned, y_aligned)[0, 1]

    # subplot settings
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    else:
        fig = None

    ax.scatter(
        x_aligned, y_aligned, color="tab:blue", alpha=0.6, s=20, label="Aligned points"
    )

    x_grid = np.linspace(x_aligned.min(), x_aligned.max(), 100)
    ax.plot(
        x_grid,
        slope * x_grid + intercept,
        color="tab:red",
        lw=1.5,
        label=f"Fit: $r = {r_val:.2f}$",
    )

    # automatical title
    title_str = f"Scatter at Peak Lag $\\tau = {peak_lag}$ months"
    if title_suffix:
        title_str += f"\n({title_suffix})"
    ax.set_title(title_str, fontsize = 14, fontweight = "bold")

    ax.set_xlabel(f"{var_names[0]} (at $t$)", fontsize = 12)
    ax.set_ylabel(f"{var_names[1]} (at $t + \\tau$)", fontsize = 12)
    ax.grid(True, linestyle = "--", alpha = 0.5)
    ax.legend(loc = "best", frameon = True)

    if fig is not None:
        fig.tight_layout()
    return fig, ax


def plot_depth_sensitivity(
    umo_dict: dict[float, xr.DataArray],
    official_time: ArrayLike | None = None,
    official_umo: ArrayLike | None = None,
    figsize: tuple[float, float] = (14, 7),
    dpi: int = 600,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot matched UMO time series for different integration depths"""

    fig, ax = plt.subplots(figsize = figsize, dpi = dpi)

    colors = {700.0: "tab:blue", 1000.0: "tab:orange", 1100.0: "tab:red"}

    if official_umo is not None and official_time is not None:
        ax.plot(
            np.asarray(official_time),
            np.asarray(official_umo, float),
            color = "gray",
            linestyle = "--",
            linewidth = 1.5,
            alpha = 0.7,
            label = "Official UMO",
        )

    # diff depths
    for z, series in umo_dict.items():
        color = colors.get(z, None)
        ax.plot(
            series.TIME.values,
            series.values,
            label = f"Calculated ($z_{{max}} = {int(z)}$ m)",
            color = color,
            linewidth = 1.2,
            alpha = 0.85,
        )

    ax.margins(x = 0.01)
    ax.set_ylim(-35, 5)
    ax.set_title(
        "Depth Sensitivity of 26°N UMO Transport", fontsize=20, fontweight="bold"
    )
    ax.set_xlabel("Time", fontsize = 16)
    ax.set_ylabel("Transport (Sv)", fontsize = 16)
    ax.grid(True, linestyle="--", alpha = 0.5)
    ax.legend(loc = "lower left", frameon = True, fontsize = 16, ncol=2)

    fig.tight_layout()
    return fig, ax
