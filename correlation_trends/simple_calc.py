from __future__ import annotations

import numpy as np
import xarray as xr
from numpy.typing import ArrayLike
from scipy import stats

from .seasonal import remove_seasonal_cycle, seasonal_climatology


def print_timeseries_info(T_UMO, official_time_axis, sample_spacing_days):

    # calculated UMO series
    t_start_umo = T_UMO.TIME.values[0]
    t_end_umo = T_UMO.TIME.values[-1]
    sampling_interval_umo = (
        T_UMO.TIME.values[1] - T_UMO.TIME.values[0]
    ) / np.timedelta64(1, "D")

    # offical UMO series
    t_start_official = official_time_axis[0]
    t_end_official = official_time_axis[-1]
    sampling_interval_official = sample_spacing_days

    # print results
    print("Calculated UMO Series")
    print(f"Time span: {t_start_umo} to {t_end_umo}")
    print(f"Total points: {len(T_UMO)}")
    print(
        f"Sampling interval: {sampling_interval_umo:.1f} days ({sampling_interval_umo * 24:.0f} hours)"
    )

    print("\nOfficial UMO Series")
    print(f"Time span: {t_start_official} to {t_end_official}")
    print(f"Total points: {len(official_time_axis)}")
    print(
        f"Sampling interval: {sampling_interval_official:.1f} days ({sampling_interval_official * 24:.0f} hours)"
    )


def report_series_correlation_and_regression(
    x: ArrayLike,
    y: ArrayLike,
    name_x: str = "Calculated",
    name_y: str = "Official",
) -> dict[str, float | int | np.ndarray]:
    """Calculate, print and return consistency metrics and linear regression parameters between 2 time series."""
    arr_x = np.asarray(x, dtype=float)
    arr_y = np.asarray(y, dtype=float)

    # filter NaN
    mask = np.isfinite(arr_x) & np.isfinite(arr_y)
    valid_x = arr_x[mask]
    valid_y = arr_y[mask]

    # calculate statistical metrics
    r, p_val = stats.pearsonr(valid_x, valid_y)
    r2 = r**2
    diff = valid_x - valid_y
    # root mean square error
    rmse = float(np.sqrt(np.mean(diff**2)))
    mean_bias = float(np.mean(diff))

    # rmse ≥ |Bias|
    # rmse^2 = bias^2 + SD_error^2
    # bias^2: systematic error contribution
    # SD_error^2: random error contribution

    # regression parameters, r-value and p-value were calculated before
    slope, intercept, _, _, stderror = stats.linregress(valid_x, valid_y)

    print("++++++Results++++++")
    print(f"Correlation between {name_x} and {name_y}")
    print("\n")
    print(f"Valid Sample Points: {valid_x.size}")
    print(f"Correlation(r): {r:.3f}(p-value: {p_val:.2e})")
    print(f"Variance Explained(R2): {r2:.1%}")
    print(f"Mean Bias ({name_x} - {name_y}): {mean_bias:+.3f} Sv")
    print(f"Root Mean Square Error: {rmse:.3f} Sv")
    print("++++++++++++++")
    print(f"\nRegression between {name_x} and {name_y}")
    print("\n")
    print(f"Linear fit: {name_y} = {slope:.3f} * {name_x} {intercept:+.3f}")
    print(f"Slope Std Error: {stderror:.3f}")
    print("++++++++++++++")

    return {
        "x": valid_x,
        "y": valid_y,
        "n_samples": int(valid_x.size),
        "r": float(r),
        "p-value": float(p_val),
        "r2": float(r2),
        "bias": mean_bias,
        "rmse": rmse,
        "slope": float(slope),
        "intercept": float(intercept),
        "stderror": float(stderror),
    }


def prepare_seasonal_and_deseasonalised_series(
    time: ArrayLike,
    trans_moc: ArrayLike,
    trans_umo: ArrayLike,
) -> dict[str, xr.DataArray]:
    """Wrap raw transport arrays into xarray.DataArray and compute climatologies and deseasonalised series."""

    # add time tag
    da_moc = xr.DataArray(trans_moc, coords={"TIME": time}, dims=["TIME"], name="MOC")
    da_umo = xr.DataArray(
        trans_umo, coords={"TIME": time}, dims=["TIME"], name="TRANS_UMO"
    )

    # climatology
    clim_moc = seasonal_climatology(da_moc)
    clim_umo = seasonal_climatology(da_umo)

    # deseasonal
    deseason_moc = remove_seasonal_cycle(da_moc)
    deseason_umo = remove_seasonal_cycle(da_umo)

    return {
        "da_moc": da_moc,
        "da_umo": da_umo,
        "clim_moc": clim_moc,
        "clim_umo": clim_umo,
        "deseason_moc": deseason_moc,
        "deseason_umo": deseason_umo,
    }


def report_trend_results(trend_res, name="SERIES"):
    """Print the trend and significance analysis report (2A.3)"""
    print(f"******** {name} INFO *************")
    print(f"Fitted Slope: {trend_res.slope:+.3f} Sv/yr")
    print(f"Intercept: {trend_res.intercept:+.3f} Sv")
    print(f"Naive Standard Error: {trend_res.se:.3f} Sv/yr")
    print(f"Effective Standard Error: {trend_res.se_eff:.3f} Sv/yr")
    print(f"Effective Sample Size (N_eff): {trend_res.n_eff:.3f}")
    print(
        f"Slope in units of its standard error (based on N_eff): {trend_res.t_eff:+.3f}"
    )
    print(f"P-value (based on N_eff): {trend_res.p_eff:.2e}")
    print(
        f"Statistically Significant (95%): {'Yes' if trend_res.p_eff < 0.05 else 'No'}\n"
    )


def match_series(
    time1: ArrayLike,
    x1: ArrayLike,
    time2: ArrayLike,
    x2: ArrayLike,
    freq: str,
) -> tuple[xr.DataArray, xr.DataArray]:
    """Resample 2 series to match freq and put both on a common time grid"""

    da1 = xr.DataArray(
        np.asarray(x1, float), coords = {"TIME": np.asarray(time1)}, dims=["TIME"]
    )
    da2 = xr.DataArray(
        np.asarray(x2, float), coords = {"TIME": np.asarray(time2)}, dims=["TIME"]
    )

    # match the freq
    da1_res = da1.resample(TIME=freq).mean()
    da2_res = da2.resample(TIME=freq).mean()

    # find common overlapping time span
    start_time = max(da1_res.TIME.values[0], da2_res.TIME.values[0])
    end_time = min(da1_res.TIME.values[-1], da2_res.TIME.values[-1])

    da1_matched = da1_res.sel(TIME = slice(start_time, end_time))
    da2_matched = da2_res.sel(TIME = slice(start_time, end_time))

    # filter unvalid datapoints
    valid = np.isfinite(da1_matched.values) & np.isfinite(da2_matched.values)
    return da1_matched.isel(TIME=valid), da2_matched.isel(TIME=valid)


def depth_sensitivity(
    ds: xr.Dataset,
    official_time: ArrayLike,
    official_umo: ArrayLike,
    depths: list[float] = [700.0, 1000.0, 1100.0],
    freq: str = "MS",
) -> dict[float, xr.DataArray]:
    """Compute and return matched UMO time series for different integration depths."""

    from correlation_trends.geostrophy import interior_geostrophic_transport

    umo_series_dict = {}

    for z in depths:
        print(f"Integration depth is {z} m")
        umo_custom = interior_geostrophic_transport(ds, z_max=z)

        # match time
        calc_matched, _ = match_series(
            umo_custom.TIME.values,
            umo_custom.values,
            official_time,
            official_umo,
            freq = freq,
        )

        umo_series_dict[z] = calc_matched

    return umo_series_dict
