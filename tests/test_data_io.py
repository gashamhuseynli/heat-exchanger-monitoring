import pandas as pd
import pytest

from heat_exchanger_monitoring.data_io import load_operating_data


def test_load_operating_data_from_valid_csv():
    data = load_operating_data("data/synthetic_operating_data.csv")

    assert data.shape == (4, 15)
    assert pd.api.types.is_datetime64_any_dtype(data["timestamp"])
    assert data["scenario"].tolist() == [
        "healthy",
        "fouling",
        "low_flow",
        "bad_sensor",
    ]


def test_load_operating_data_rejects_missing_columns(tmp_path):
    invalid_csv = tmp_path / "invalid_data.csv"
    invalid_csv.write_text(
        "timestamp,scenario\n"
        "2026-11-01 08:00:00,healthy\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        load_operating_data(invalid_csv)