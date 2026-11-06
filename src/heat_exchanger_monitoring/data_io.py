from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = (
    "timestamp",
    "scenario",
    "hot_mass_flow_kg_s",
    "cold_mass_flow_kg_s",
    "hot_cp_kj_kg_k",
    "cold_cp_kj_kg_k",
    "hot_inlet_temp_c",
    "hot_outlet_temp_c",
    "cold_inlet_temp_c",
    "cold_outlet_temp_c",
    "hot_inlet_pressure_kpa",
    "hot_outlet_pressure_kpa",
    "cold_inlet_pressure_kpa",
    "cold_outlet_pressure_kpa",
    "area_m2",
)


def load_operating_data(csv_path: str | Path) -> pd.DataFrame:
    """Load operating data and verify that all required columns exist."""
    data = pd.read_csv(csv_path)

    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)

    if missing_columns:
        formatted_columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {formatted_columns}")

    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="raise")

    return data