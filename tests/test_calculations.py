import numpy as np

from heat_exchanger_monitoring.calculations import calculate_hot_duty


def test_calculate_hot_duty_for_multiple_cases():
    mass_flow_kg_s = np.array([2.0, 2.0, 1.5])
    cp_kj_kg_k = 4.0
    inlet_temp_c = np.array([150.0, 140.0, 130.0])
    outlet_temp_c = np.array([100.0, 100.0, 100.0])
    expected_duty_kw = np.array([400.0, 320.0, 180.0])

    actual_duty_kw = calculate_hot_duty(
        mass_flow_kg_s,
        cp_kj_kg_k,
        inlet_temp_c,
        outlet_temp_c,
    )

    assert np.isclose(actual_duty_kw, expected_duty_kw).all()
