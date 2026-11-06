import numpy as np
import pandas as pd

from heat_exchanger_monitoring.calculations import (
    calculate_cold_duty,
    calculate_counter_current_lmtd,
    calculate_energy_balance_deviation,
    calculate_hot_duty,
    calculate_u,
    calculate_ua,
)
from heat_exchanger_monitoring.validation import validate_operating_data


RESULT_COLUMNS = (
    "hot_duty_kw",
    "cold_duty_kw",
    "average_duty_kw",
    "energy_balance_deviation_percent",
    "lmtd_c",
    "ua_kw_per_k",
    "u_w_m2_k",
    "hot_pressure_drop_kpa",
    "cold_pressure_drop_kpa",
)


def analyze_operating_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate operating data and calculate performance indicators."""
    results = validate_operating_data(data)

    for column in RESULT_COLUMNS:
        results[column] = np.nan

    valid_mask = results["is_valid"]
    valid_data = results.loc[valid_mask]

    if valid_data.empty:
        return results

    hot_duty_kw = calculate_hot_duty(
        valid_data["hot_mass_flow_kg_s"].to_numpy(),
        valid_data["hot_cp_kj_kg_k"].to_numpy(),
        valid_data["hot_inlet_temp_c"].to_numpy(),
        valid_data["hot_outlet_temp_c"].to_numpy(),
    )

    cold_duty_kw = calculate_cold_duty(
        valid_data["cold_mass_flow_kg_s"].to_numpy(),
        valid_data["cold_cp_kj_kg_k"].to_numpy(),
        valid_data["cold_inlet_temp_c"].to_numpy(),
        valid_data["cold_outlet_temp_c"].to_numpy(),
    )

    average_duty_kw = (hot_duty_kw + cold_duty_kw) / 2.0

    energy_deviation_percent = calculate_energy_balance_deviation(
        hot_duty_kw,
        cold_duty_kw,
    )

    lmtd_c = calculate_counter_current_lmtd(
        valid_data["hot_inlet_temp_c"].to_numpy(),
        valid_data["hot_outlet_temp_c"].to_numpy(),
        valid_data["cold_inlet_temp_c"].to_numpy(),
        valid_data["cold_outlet_temp_c"].to_numpy(),
    )

    ua_kw_per_k = calculate_ua(average_duty_kw, lmtd_c)

    u_w_m2_k = calculate_u(
        ua_kw_per_k,
        valid_data["area_m2"].to_numpy(),
    )

    results.loc[valid_mask, "hot_duty_kw"] = hot_duty_kw
    results.loc[valid_mask, "cold_duty_kw"] = cold_duty_kw
    results.loc[valid_mask, "average_duty_kw"] = average_duty_kw
    results.loc[
        valid_mask, "energy_balance_deviation_percent"
    ] = energy_deviation_percent
    results.loc[valid_mask, "lmtd_c"] = lmtd_c
    results.loc[valid_mask, "ua_kw_per_k"] = ua_kw_per_k
    results.loc[valid_mask, "u_w_m2_k"] = u_w_m2_k

    results.loc[valid_mask, "hot_pressure_drop_kpa"] = (
        valid_data["hot_inlet_pressure_kpa"]
        - valid_data["hot_outlet_pressure_kpa"]
    )

    results.loc[valid_mask, "cold_pressure_drop_kpa"] = (
        valid_data["cold_inlet_pressure_kpa"]
        - valid_data["cold_outlet_pressure_kpa"]
    )

    return results