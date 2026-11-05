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

def calculate_counter_current_lmtd(
    hot_inlet_temp_c: np.ndarray,
    hot_outlet_temp_c: np.ndarray,
    cold_inlet_temp_c: np.ndarray,
    cold_outlet_temp_c: np.ndarray,
) -> np.ndarray:
    """Calculate counter-current LMTD in degrees Celsius."""
    delta_t_1 = hot_inlet_temp_c - cold_outlet_temp_c
    delta_t_2 = hot_outlet_temp_c - cold_inlet_temp_c

    if np.any(delta_t_1 <= 0) or np.any(delta_t_2 <= 0):
        raise ValueError("Terminal temperature differences must be positive.")

    lmtd = np.empty_like(delta_t_1, dtype=float)
    equal_mask = np.isclose(delta_t_1, delta_t_2)

    lmtd[equal_mask] = delta_t_1[equal_mask]
    lmtd[~equal_mask] = (
        (delta_t_1[~equal_mask] - delta_t_2[~equal_mask])
        / np.log(delta_t_1[~equal_mask] / delta_t_2[~equal_mask])
    )

    return lmtd

def calculate_ua(
    duty_kw: np.ndarray,
    lmtd_c: np.ndarray,
) -> np.ndarray:
    """Calculate UA in kW/K from heat duty and LMTD."""
    if np.any(duty_kw < 0):
        raise ValueError("Heat duty must be non-negative.")

    if np.any(lmtd_c <= 0):
        raise ValueError("LMTD must be positive.")

    return duty_kw / lmtd_c


def calculate_u(
    ua_kw_per_k: np.ndarray,
    area_m2: np.ndarray,
) -> np.ndarray:
    """Calculate overall heat-transfer coefficient in W/(m²·K)."""
    if np.any(ua_kw_per_k < 0):
        raise ValueError("UA must be non-negative.")

    if np.any(area_m2 <= 0):
        raise ValueError("Area must be positive.")

    return ua_kw_per_k * 1000.0 / area_m2