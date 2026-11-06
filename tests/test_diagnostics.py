import pytest

from heat_exchanger_monitoring.analysis import analyze_operating_data
from heat_exchanger_monitoring.data_io import load_operating_data
from heat_exchanger_monitoring.diagnostics import screen_faults


def test_fault_screening_classifies_synthetic_scenarios():
    data = load_operating_data("data/synthetic_operating_data.csv")
    analyzed_data = analyze_operating_data(data)

    results = screen_faults(analyzed_data)
    statuses = results.set_index("scenario")["diagnostic_status"]

    assert statuses["healthy"] == "normal"
    assert statuses["fouling"] == "possible_fouling"
    assert statuses["low_flow"] == "possible_low_flow"
    assert statuses["bad_sensor"] == "invalid_data"


def test_fault_screening_requires_healthy_reference():
    data = load_operating_data("data/synthetic_operating_data.csv")
    analyzed_data = analyze_operating_data(data)

    with pytest.raises(
        ValueError,
        match="valid healthy reference",
    ):
        screen_faults(
            analyzed_data,
            reference_scenario="missing_reference",
        )