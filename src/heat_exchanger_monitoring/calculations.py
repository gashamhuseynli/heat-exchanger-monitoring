import numpy as np


def calculate_hot_duty(
    mass_flow_kg_s: np.ndarray,
    cp_kj_kg_k: float,
    inlet_temp_c: np.ndarray,
    outlet_temp_c: np.ndarray,
) -> np.ndarray:
    """Calculate positive hot-side heat duty in kW."""
    delta_temp_k = inlet_temp_c - outlet_temp_c
    return mass_flow_kg_s * cp_kj_kg_k * delta_temp_k

def calculate_cold_duty(
    mass_flow_kg_s: np.ndarray,
    cp_kj_kg_k: float,
    inlet_temp_c: np.ndarray,
    outlet_temp_c: np.ndarray,
) -> np.ndarray:
    """Calculate positive cold-side heat duty in kW."""
    delta_temp_k = outlet_temp_c - inlet_temp_c
    return mass_flow_kg_s * cp_kj_kg_k * delta_temp_k

def calculate_energy_balance_deviation(
    hot_duty_kw: np.ndarray,
    cold_duty_kw: np.ndarray,
) -> np.ndarray:
    """Calculate symmetric hot/cold duty deviation in percent."""
    average_duty_kw = (hot_duty_kw + cold_duty_kw) / 2.0
    absolute_difference_kw = np.abs(hot_duty_kw - cold_duty_kw)
    return absolute_difference_kw / average_duty_kw * 100.0
