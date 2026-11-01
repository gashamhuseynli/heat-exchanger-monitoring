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
