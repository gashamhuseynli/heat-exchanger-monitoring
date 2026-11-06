import numpy as np
import pandas as pd


MAX_ENERGY_DEVIATION_PERCENT = 10.0
LOW_FLOW_RATIO_PERCENT = 80.0
LOW_U_RATIO_PERCENT = 85.0
HIGH_PRESSURE_DROP_RATIO_PERCENT = 120.0


def screen_faults(
    analyzed_data: pd.DataFrame,
    reference_scenario: str = "healthy",
) -> pd.DataFrame:
    """Compare valid rows with a healthy reference and screen possible faults."""
    screened_data = analyzed_data.copy()

    reference_rows = screened_data.loc[
        (screened_data["scenario"] == reference_scenario)
        & screened_data["is_valid"]
    ]

    if reference_rows.empty:
        raise ValueError("A valid healthy reference row is required")

    reference = reference_rows.iloc[0]
    valid_mask = screened_data["is_valid"]

    ratio_columns = (
        "u_ratio_percent",
        "hot_flow_ratio_percent",
        "cold_flow_ratio_percent",
        "hot_pressure_drop_ratio_percent",
        "cold_pressure_drop_ratio_percent",
    )

    for column in ratio_columns:
        screened_data[column] = np.nan

    screened_data.loc[valid_mask, "u_ratio_percent"] = (
        screened_data.loc[valid_mask, "u_w_m2_k"]
        / reference["u_w_m2_k"]
        * 100.0
    )

    screened_data.loc[valid_mask, "hot_flow_ratio_percent"] = (
        screened_data.loc[valid_mask, "hot_mass_flow_kg_s"]
        / reference["hot_mass_flow_kg_s"]
        * 100.0
    )

    screened_data.loc[valid_mask, "cold_flow_ratio_percent"] = (
        screened_data.loc[valid_mask, "cold_mass_flow_kg_s"]
        / reference["cold_mass_flow_kg_s"]
        * 100.0
    )

    screened_data.loc[
        valid_mask, "hot_pressure_drop_ratio_percent"
    ] = (
        screened_data.loc[valid_mask, "hot_pressure_drop_kpa"]
        / reference["hot_pressure_drop_kpa"]
        * 100.0
    )

    screened_data.loc[
        valid_mask, "cold_pressure_drop_ratio_percent"
    ] = (
        screened_data.loc[valid_mask, "cold_pressure_drop_kpa"]
        / reference["cold_pressure_drop_kpa"]
        * 100.0
    )

    statuses = []
    messages = []

    for _, row in screened_data.iterrows():
        if not row["is_valid"]:
            status = "invalid_data"
            message = row["validation_message"]

        elif (
            row["energy_balance_deviation_percent"]
            > MAX_ENERGY_DEVIATION_PERCENT
        ):
            status = "energy_imbalance"
            message = "Hot-side and cold-side duties differ significantly"

        elif (
            row["hot_flow_ratio_percent"] < LOW_FLOW_RATIO_PERCENT
            and row["hot_pressure_drop_ratio_percent"]
            < LOW_FLOW_RATIO_PERCENT
        ) or (
            row["cold_flow_ratio_percent"] < LOW_FLOW_RATIO_PERCENT
            and row["cold_pressure_drop_ratio_percent"]
            < LOW_FLOW_RATIO_PERCENT
        ):
            status = "possible_low_flow"
            message = "Reduced flow and pressure drop indicate possible low flow"

        elif (
            row["u_ratio_percent"] < LOW_U_RATIO_PERCENT
            and (
                row["hot_pressure_drop_ratio_percent"]
                > HIGH_PRESSURE_DROP_RATIO_PERCENT
                or row["cold_pressure_drop_ratio_percent"]
                > HIGH_PRESSURE_DROP_RATIO_PERCENT
            )
        ):
            status = "possible_fouling"
            message = (
                "Reduced U with increased pressure drop indicates "
                "possible fouling or flow restriction"
            )

        elif row["u_ratio_percent"] < LOW_U_RATIO_PERCENT:
            status = "reduced_heat_transfer"
            message = "Overall heat-transfer performance is below reference"

        else:
            status = "normal"
            message = "Operation is within the defined reference thresholds"

        statuses.append(status)
        messages.append(message)

    screened_data["diagnostic_status"] = statuses
    screened_data["diagnostic_message"] = messages

    return screened_data