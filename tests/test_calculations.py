import numpy as np

from heat_exchanger_monitoring.calculations import calculate_cold_duty
from heat_exchanger_monitoring.calculations import calculate_hot_duty
from heat_exchanger_monitoring.calculations import calculate_energy_balance_deviation

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


def test_calculate_cold_duty_for_multiple_cases():
    mass_flow_kg_s = np.array([2.5, 2.0, 1.5])
    cp_kj_kg_k = 4.0
    inlet_temp_c = np.array([30.0, 35.0, 40.0])
    outlet_temp_c = np.array([70.0, 75.0, 70.0])
    expected_duty_kw = np.array([400.0, 320.0, 180.0])

    actual_duty_kw = calculate_cold_duty(
        mass_flow_kg_s,
        cp_kj_kg_k,
        inlet_temp_c,
        outlet_temp_c,
    )

    assert np.isclose(actual_duty_kw, expected_duty_kw).all()

def test_calculate_energy_balance_deviation():
    hot_duty_kw = np.array([400.0, 320.0, 180.0])
    cold_duty_kw = np.array([400.0, 304.0, 198.0])
    expected_deviation_percent = np.array(
        [0.0, 5.128205128205129, 9.523809523809524]
    )

    actual_deviation_percent = calculate_energy_balance_deviation(
        hot_duty_kw,
        cold_duty_kw,
    )

    assert np.isclose(
        actual_deviation_percent,
        expected_deviation_percent,
    ).all()
