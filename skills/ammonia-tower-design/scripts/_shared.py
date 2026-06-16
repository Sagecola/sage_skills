"""Shared constants, types, and utility functions for ammonia tower design scripts.

Import this module instead of importing from calculate_two_stage_ammonia_towers
to avoid circular dependencies between the calculation engine sub-modules.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# --- Physical and mathematical constants ---

SMALL = 1e-12
G = 9.81  # m/s2
G_HOUR = G * 3600.0 * 3600.0  # m/h2 (for Onda correlations)
PA_PER_IN_H2O = 249.08891
M_PER_FT = 0.3048
FT_PER_M = 1.0 / M_PER_FT
LB_PER_KG = 2.20462
CP_PER_PA_S = 1000.0
G_FT_S2 = 32.2  # gravitational constant in ft/s2

# --- Molecular weights ---

MW_N = 14.007
MW_NH3 = 17.031
MW_H2O = 18.015
MW_HCL = 36.46

R_KPA_M3_PER_KMOL_K = 8.314462618
P_ATM_KPA = 101.325


# --- Dataclasses ---

@dataclass
class TowerHydraulics:
    gas_flow_m3_h: float
    liquid_flow_m3_h: float
    operating_velocity_m_s: float
    flooding_velocity_m_s: float | None
    flooding_fraction: float | None
    cross_section_m2: float
    tower_diameter_m: float
    pressure_drop_pa_m: float | None
    spray_density_m3_m2_h: float
    min_spray_density_m3_m2_h: float
    min_liquid_flow_m3_h: float


# --- Utility functions ---

def diameter_from_flow(gas_flow_m3_h: float, superficial_velocity_m_s: float) -> tuple[float, float]:
    """Calculate tower diameter and cross-section from gas flow and superficial velocity."""
    gas_flow_m3_s = gas_flow_m3_h / 3600.0
    area_m2 = gas_flow_m3_s / superficial_velocity_m_s
    diameter_m = math.sqrt(4.0 * area_m2 / math.pi)
    return diameter_m, area_m2


def suggested_nominal_diameter_m(calculated_diameter_m: float) -> float:
    """Round up to a practical shell diameter.

    JB1153-73 style rounding:
    - below 1.0 m: use 0.1 m increments
    - 1.0 m and above: use 0.2 m increments
    """
    step = 0.1 if calculated_diameter_m < 1.0 else 0.2
    return math.ceil((calculated_diameter_m - SMALL) / step) * step


def gas_molar_volume_m3_per_kmol(temperature_c: float, pressure_kpa: float) -> float:
    """Ideal gas molar volume at given temperature and pressure."""
    temperature_k = temperature_c + 273.15
    return R_KPA_M3_PER_KMOL_K * temperature_k / pressure_kpa


def pa_s_to_kg_m_h(value_pa_s: float) -> float:
    """Convert Pa·s to kg/(m·h)."""
    return value_pa_s * 3600.0


def dyn_cm_to_kg_h2(value_dyn_cm: float) -> float:
    """Convert dyn/cm to kg/h²."""
    return value_dyn_cm * 12960.0


def in_h2o_ft_to_pa_m(value_in_h2o_ft: float) -> float:
    """Convert inH₂O/ft to Pa/m."""
    return value_in_h2o_ft * PA_PER_IN_H2O / M_PER_FT
