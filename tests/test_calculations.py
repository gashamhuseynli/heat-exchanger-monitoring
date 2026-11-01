import numpy as np
import pytest

from heat_exchanger_monitoring.calculations import (
    calculate_cold_duty,
    calculate_counter_current_lmtd,
    calculate_energy_balance_deviation,
    calculate_hot_duty,
)

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

def test_calculate_counter_current_lmtd():
    hot_inlet_temp_c = np.array([150.0, 130.0])
    hot_outlet_temp_c = np.array([100.0, 90.0])
    cold_inlet_temp_c = np.array([60.0, 40.0])
    cold_outlet_temp_c = np.array([70.0, 80.0])

    expected_lmtd_c = np.array([
        40.0 / np.log(2.0),
        50.0,
    ])

    actual_lmtd_c = calculate_counter_current_lmtd(
        hot_inlet_temp_c,
        hot_outlet_temp_c,
        cold_inlet_temp_c,
        cold_outlet_temp_c,
    )

    assert np.allclose(actual_lmtd_c, expected_lmtd_c)


def test_lmtd_rejects_nonpositive_temperature_difference():
    with pytest.raises(ValueError, match="must be positive"):
        calculate_counter_current_lmtd(
            np.array([80.0]),
            np.array([70.0]),
            np.array([75.0]),
            np.array([85.0]),
        )