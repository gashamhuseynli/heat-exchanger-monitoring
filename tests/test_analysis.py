import numpy as np

from heat_exchanger_monitoring.analysis import analyze_operating_data
from heat_exchanger_monitoring.data_io import load_operating_data


def test_analysis_calculates_healthy_case():
    data = load_operating_data("data/synthetic_operating_data.csv")

    results = analyze_operating_data(data)
    healthy = results.loc[results["scenario"] == "healthy"].iloc[0]

    assert np.isclose(healthy["hot_duty_kw"], 400.0)
    assert np.isclose(healthy["cold_duty_kw"], 400.0)
    assert np.isclose(
        healthy["energy_balance_deviation_percent"],
        0.0,
    )
    assert np.isclose(healthy["hot_pressure_drop_kpa"], 40.0)
    assert np.isclose(healthy["cold_pressure_drop_kpa"], 35.0)


def test_analysis_skips_invalid_row():
    data = load_operating_data("data/synthetic_operating_data.csv")

    results = analyze_operating_data(data)
    bad_sensor = results.loc[
        results["scenario"] == "bad_sensor"
    ].iloc[0]

    assert not bad_sensor["is_valid"]
    assert np.isnan(bad_sensor["hot_duty_kw"])
    assert np.isnan(bad_sensor["lmtd_c"])
    assert np.isnan(bad_sensor["u_w_m2_k"])