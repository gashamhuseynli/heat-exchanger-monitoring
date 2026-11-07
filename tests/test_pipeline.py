import pandas as pd

from heat_exchanger_monitoring.pipeline import run_monitoring_pipeline


def test_run_monitoring_pipeline(tmp_path):
    output_path = tmp_path / "analysis_results.csv"

    results = run_monitoring_pipeline(
        "data/synthetic_operating_data.csv",
        output_csv=output_path,
    )

    assert output_path.exists()
    assert len(results) == 4

    statuses = results.set_index("scenario")["diagnostic_status"]

    assert statuses["healthy"] == "normal"
    assert statuses["fouling"] == "possible_fouling"
    assert statuses["low_flow"] == "possible_low_flow"
    assert statuses["bad_sensor"] == "invalid_data"

    saved_results = pd.read_csv(output_path)

    assert len(saved_results) == 4
    assert "diagnostic_status" in saved_results.columns