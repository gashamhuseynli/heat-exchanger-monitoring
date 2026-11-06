import pandas as pd

from heat_exchanger_monitoring.data_io import REQUIRED_COLUMNS


POSITIVE_COLUMNS = (
    "hot_mass_flow_kg_s",
    "cold_mass_flow_kg_s",
    "hot_cp_kj_kg_k",
    "cold_cp_kj_kg_k",
    "area_m2",
)


def validate_operating_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate each operating-data row using basic engineering constraints."""
    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)

    if missing_columns:
        formatted_columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {formatted_columns}")

    validated_data = data.copy()
    row_issues = [[] for _ in range(len(validated_data))]

    def add_issue(condition: pd.Series, message: str) -> None:
        for position, failed in enumerate(condition.fillna(False)):
            if failed:
                row_issues[position].append(message)

    add_issue(
        validated_data[list(REQUIRED_COLUMNS)].isna().any(axis=1),
        "missing required value",
    )

    add_issue(
        validated_data["timestamp"].duplicated(keep=False),
        "duplicate timestamp",
    )

    add_issue(
        (validated_data[list(POSITIVE_COLUMNS)] <= 0).any(axis=1),
        "mass flow, heat capacity and area must be positive",
    )

    add_issue(
        validated_data["hot_outlet_temp_c"]
        >= validated_data["hot_inlet_temp_c"],
        "hot outlet temperature must be lower than hot inlet temperature",
    )

    add_issue(
        validated_data["cold_outlet_temp_c"]
        <= validated_data["cold_inlet_temp_c"],
        "cold outlet temperature must be higher than cold inlet temperature",
    )

    add_issue(
        (
            validated_data["hot_outlet_pressure_kpa"]
            >= validated_data["hot_inlet_pressure_kpa"]
        )
        | (
            validated_data["cold_outlet_pressure_kpa"]
            >= validated_data["cold_inlet_pressure_kpa"]
        ),
        "inlet pressure must be higher than outlet pressure",
    )

    add_issue(
        (
            validated_data["hot_inlet_temp_c"]
            - validated_data["cold_outlet_temp_c"]
            <= 0
        )
        | (
            validated_data["hot_outlet_temp_c"]
            - validated_data["cold_inlet_temp_c"]
            <= 0
        ),
        "counter-current terminal temperature differences must be positive",
    )

    validated_data["is_valid"] = [
        len(issues) == 0 for issues in row_issues
    ]

    validated_data["validation_message"] = [
        "valid" if not issues else "; ".join(issues)
        for issues in row_issues
    ]

    return validated_data