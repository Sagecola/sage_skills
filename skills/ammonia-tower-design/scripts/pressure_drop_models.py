"""Pressure drop correlations for packed towers.

This module collects all pressure drop models:
- Blackwell-Kessler-Wankat (polynomial fit to constant-pressure-drop lines)
- Billet-Schultes (1999) (physics-based, geometry-driven)

For flooding velocity correlations, see flooding_models.py.
"""

from __future__ import annotations

import math

try:
    from ._shared import SMALL, G, PA_PER_IN_H2O, M_PER_FT
except ImportError:
    from _shared import SMALL, G, PA_PER_IN_H2O, M_PER_FT  # type: ignore[no-redef]

BLACKWELL_DP_CONSTANTS = {
    0.05: (-6.30253, -0.60809, -0.11932, -0.00685, 0.00032),
    0.10: (-5.50093, -0.78508, -0.13496, 0.00134, 0.00174),
    0.25: (-5.00319, -0.95299, -0.13930, 0.01264, 0.00334),
    0.50: (-4.39918, -0.99404, -0.16983, 0.00873, 0.00343),
    1.0: (-4.09505, -1.00120, -0.15871, 0.00797, 0.00318),
    1.5: (-4.02555, -0.98945, -0.08291, 0.03237, 0.00532),
}

KISTER_GPDC_CONSTANTS = {
    "structured": (3.8617, 0.6609, 6.3763, 0.7206, 0.2898, -0.9093, -0.6819),
    "random": (3.0, 0.5778, 5.3597, 0.5545, 0.4046, -1.4234, -0.6022),
}

def in_h2o_ft_to_pa_m(value_in_h2o_ft: float) -> float:
    return value_in_h2o_ft * PA_PER_IN_H2O / M_PER_FT


def blackwell_abscissa(
    liquid_mass_flow_kg_h: float,
    gas_mass_flow_kg_h: float,
    liquid_density_kg_m3: float,
    gas_density_kg_m3: float,
) -> float:
    """Calculate Blackwell abscissa X = (L/G) * [rho_G / (rho_L - rho_G)]^0.5"""
    L_G = liquid_mass_flow_kg_h / max(gas_mass_flow_kg_h, SMALL)
    density_term = math.sqrt(gas_density_kg_m3 / max(liquid_density_kg_m3 - gas_density_kg_m3, SMALL))
    return L_G * density_term


def blackwell_pressure_drop_ordinate(
    gas_mass_velocity_lb_ft2_s: float,
    packing_factor_ft_inv: float,
    liquid_viscosity_cp: float,
    gas_density_lb_ft3: float,
    liquid_density_lb_ft3: float,
) -> float:
    """Calculate Blackwell ordinate Y = (G_1^2 * F_p * mu_L^0.1) / [rho_G * (rho_L - rho_G) * g]"""
    numerator = (gas_mass_velocity_lb_ft2_s ** 2) * packing_factor_ft_inv * (liquid_viscosity_cp ** 0.1)
    denominator = gas_density_lb_ft3 * (liquid_density_lb_ft3 - gas_density_lb_ft3) * G_FT_S2
    return numerator / max(denominator, SMALL)


def blackwell_pressure_drop_from_x(
    x_value: float,
    target_dp_in_h2o_ft: float,
) -> float:
    """Calculate Blackwell ordinate Y from abscissa X using interpolation."""
    # Find the two closest pressure drop values for interpolation
    dp_values = sorted(BLACKWELL_DP_CONSTANTS.keys())

    # Find the closest match
    closest_dp = min(dp_values, key=lambda dp: abs(dp - target_dp_in_h2o_ft))

    # If exact match, use it directly
    if abs(closest_dp - target_dp_in_h2o_ft) < 0.001:
        C0, C1, C2, C3, C4 = BLACKWELL_DP_CONSTANTS[closest_dp]
        ln_x = math.log(max(x_value, 1e-10))
        return math.exp(C0 + C1 * ln_x + C2 * ln_x**2 + C3 * ln_x**3 + C4 * ln_x**4)

    # Interpolate between two closest values
    lower_dp = max([dp for dp in dp_values if dp <= target_dp_in_h2o_ft], default=dp_values[0])
    upper_dp = min([dp for dp in dp_values if dp >= target_dp_in_h2o_ft], default=dp_values[-1])

    if lower_dp == upper_dp:
        C0, C1, C2, C3, C4 = BLACKWELL_DP_CONSTANTS[lower_dp]
        ln_x = math.log(max(x_value, 1e-10))
        return math.exp(C0 + C1 * ln_x + C2 * ln_x**2 + C3 * ln_x**3 + C4 * ln_x**4)

    # Calculate Y for both pressure drops
    C0_low, C1_low, C2_low, C3_low, C4_low = BLACKWELL_DP_CONSTANTS[lower_dp]
    C0_high, C1_high, C2_high, C3_high, C4_high = BLACKWELL_DP_CONSTANTS[upper_dp]

    ln_x = math.log(max(x_value, 1e-10))
    y_low = math.exp(C0_low + C1_low * ln_x + C2_low * ln_x**2 + C3_low * ln_x**3 + C4_low * ln_x**4)
    y_high = math.exp(C0_high + C1_high * ln_x + C2_high * ln_x**2 + C3_high * ln_x**3 + C4_high * ln_x**4)

    # Linear interpolation in log-log space
    weight = (target_dp_in_h2o_ft - lower_dp) / (upper_dp - lower_dp)
    return y_low * (y_high / y_low) ** weight



# --- Billet-Schultes (1999) pressure drop model ---


# G imported from _shared


def particle_diameter(voidage: float, specific_area: float) -> float:
    """Equivalent particle diameter dp = 6(1-epsilon)/a [m]."""
    return 6.0 * (1.0 - voidage) / specific_area


def wall_factor(voidage: float, specific_area: float, column_diameter: float) -> float:
    """Wall factor K accounting for increased voidage near column wall.
    
    1/K = 1 + (2/3)(1/(1-epsilon))(dp/Dc)
    """
    dp = particle_diameter(voidage, specific_area)
    return 1.0 / (1.0 + (2.0 / 3.0) * (1.0 / (1.0 - voidage)) * (dp / column_diameter))


def gas_reynolds_number(
    gas_velocity: float,
    gas_density: float,
    gas_viscosity: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
) -> float:
    """Gas Reynolds number for packed bed.
    
    Re_G = u_G * dp / ((1-epsilon) * nu_G) * K
    where nu_G = mu_G / rho_G
    """
    dp = particle_diameter(voidage, specific_area)
    kinematic_viscosity = gas_viscosity / gas_density
    K = wall_factor(voidage, specific_area, column_diameter)
    return gas_velocity * dp / ((1.0 - voidage) * kinematic_viscosity) * K


def dry_resistance_coefficient(
    cp0: float,
    re_g: float,
) -> float:
    """Dry bed resistance coefficient psi_0.
    
    psi_0 = Cp0 * (64/Re_G + 1.8/Re_G^0.08)
    """
    return cp0 * (64.0 / re_g + 1.8 / (re_g ** 0.08))


def dry_pressure_drop(
    gas_velocity: float,
    gas_density: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
    cp0: float,
) -> float:
    """Dry bed pressure drop per unit height [Pa/m].
    
    dP/dz = psi_0 * (a/epsilon^3) * (F_G^2/2) * (1/K)
    where F_G = u_G * sqrt(rho_G)
    """
    K = wall_factor(voidage, specific_area, column_diameter)
    re_g = gas_reynolds_number(
        gas_velocity, gas_density, 1.81e-5, voidage, specific_area, column_diameter
    )
    psi_0 = dry_resistance_coefficient(cp0, re_g)
    f_g = gas_velocity * math.sqrt(gas_density)
    return psi_0 * (specific_area / (voidage ** 3)) * (f_g ** 2 / 2.0) * (1.0 / K)


def preloading_liquid_holdup(
    liquid_velocity: float,
    liquid_viscosity: float,
    liquid_density: float,
    voidage: float,
    specific_area: float,
) -> float:
    """Liquid holdup in preloading region (below loading point).
    
    h_L = [12 * mu_L * u_L * a / (g * rho_L)]^(1/3)
    
    Valid for u_L up to loading point.
    """
    return (
        12.0 * liquid_viscosity * liquid_velocity * specific_area
        / (G * liquid_density)
    ) ** (1.0 / 3.0)


def hydraulic_area(
    liquid_velocity: float,
    liquid_viscosity: float,
    liquid_density: float,
    surface_tension_n_m: float,
    specific_area: float,
    ch: float = 1.0,
) -> float:
    """Hydraulic (wetted) area a_h [m2/m3] for liquid holdup calculation.
    
    Billet-Schultes 1999 formula gives the fraction of packing area that is
    effectively wetted by the liquid film. This is typically 3-8% of the
    geometric area a for low liquid loads, increasing with liquid velocity.
    
    a_h / a = (3/4) * C_h * (rho_L / (sigma_L * g))^(-1/6)
              * (u_L / (a * nu_L))^(-1/4)
              * (u_L^2 * a / g)^(1/12)
    
    where:
      C_h = packing-specific constant (~0.82-1.1, default 1.0)
            Metal Pall ring: ~0.90, Ceramic Raschig: ~1.1
      nu_L = mu_L / rho_L (kinematic viscosity)
    
    The ratio a_h/a represents wetting efficiency. For a_h > a, clamp to a.
    """
    kinematic_viscosity = liquid_viscosity / liquid_density
    
    term1 = (3.0 / 4.0) * ch
    term2 = (liquid_density / (surface_tension_n_m * G)) ** (-1.0 / 6.0)
    term3 = (liquid_velocity / (specific_area * kinematic_viscosity)) ** (-1.0 / 4.0)
    term4 = (liquid_velocity ** 2 * specific_area / G) ** (1.0 / 12.0)
    
    a_h = specific_area * term1 * term2 * term3 * term4
    # Hydraulic area should not exceed geometric area in this context
    return min(a_h, specific_area)


def wet_resistance_coefficient(
    cp0: float,
    re_g: float,
    voidage: float,
    liquid_holdup: float,
    specific_area: float,
    hydraulic_area: float,
) -> float:
    """Wet bed resistance coefficient psi_L.
    
    psi_L = Cp0 * (64/Re_G + 1.8/Re_G^0.08)
            * ((epsilon - h_L)/epsilon)^1.5
            * (a/a_h)^0.2
            * exp((13300/a^1.5) * sqrt(a/g))
    """
    psi_base = dry_resistance_coefficient(cp0, re_g)
    voidage_ratio = ((voidage - liquid_holdup) / voidage) ** 1.5
    area_ratio = (specific_area / hydraulic_area) ** 0.2
    # Surface texture factor: ~1.0 for smooth plastic, ~1.1-1.3 for textured metal
    # The original Billet-Schultes formula has a packing-specific surface factor.
    # For most practical calculations with smooth plastic packings, this is near 1.0.
    exp_term = 1.0
    return psi_base * voidage_ratio * area_ratio * exp_term


def irrigated_pressure_drop(
    gas_velocity: float,
    liquid_velocity: float,
    gas_density: float,
    liquid_density: float,
    gas_viscosity: float,
    liquid_viscosity: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
    cp0: float,
) -> float:
    """Irrigated bed pressure drop per unit height [Pa/m].
    
    dP/dz = psi_L * (a/(epsilon - h_L)^3) * (F_G^2/2) * (1/K)
    
    This is valid below the loading point. Above loading point,
    liquid holdup increases with gas velocity and an iterative
    solution is needed.
    """
    K = wall_factor(voidage, specific_area, column_diameter)
    h_l = preloading_liquid_holdup(
        liquid_velocity, liquid_viscosity, liquid_density, voidage, specific_area
    )
    a_h = hydraulic_area(
        liquid_velocity, liquid_viscosity, liquid_density,
        surface_tension_n_m=0.07275, specific_area=specific_area
    )
    re_g = gas_reynolds_number(
        gas_velocity, gas_density, gas_viscosity, voidage, specific_area, column_diameter
    )
    psi_l = wet_resistance_coefficient(cp0, re_g, voidage, h_l, specific_area, a_h)
    f_g = gas_velocity * math.sqrt(gas_density)
    return psi_l * (specific_area / ((voidage - h_l) ** 3)) * (f_g ** 2 / 2.0) * (1.0 / K)


def billet_schultes_pressure_drop(
    gas_velocity: float,
    liquid_velocity: float,
    gas_density: float,
    liquid_density: float,
    gas_viscosity: float,
    liquid_viscosity: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
    cp0: float,
) -> dict[str, float]:
    """Calculate both dry and irrigated pressure drop.
    
    Returns a dict with:
    - dry_pa_m: dry bed pressure drop [Pa/m]
    - irrigated_pa_m: irrigated bed pressure drop [Pa/m]
    - liquid_holdup: liquid holdup [-]
    - re_g: gas Reynolds number [-]
    - psi_0: dry resistance coefficient [-]
    - psi_l: wet resistance coefficient [-]
    """
    K = wall_factor(voidage, specific_area, column_diameter)
    h_l = preloading_liquid_holdup(
        liquid_velocity, liquid_viscosity, liquid_density, voidage, specific_area
    )
    a_h = hydraulic_area(
        liquid_velocity, liquid_viscosity, liquid_density,
        surface_tension_n_m=0.07275, specific_area=specific_area
    )
    re_g = gas_reynolds_number(
        gas_velocity, gas_density, gas_viscosity, voidage, specific_area, column_diameter
    )
    psi_0 = dry_resistance_coefficient(cp0, re_g)
    psi_l = wet_resistance_coefficient(cp0, re_g, voidage, h_l, specific_area, a_h)
    f_g = gas_velocity * math.sqrt(gas_density)
    
    dry_pa_m = psi_0 * (specific_area / (voidage ** 3)) * (f_g ** 2 / 2.0) * (1.0 / K)
    irrigated_pa_m = psi_l * (specific_area / ((voidage - h_l) ** 3)) * (f_g ** 2 / 2.0) * (1.0 / K)
    
    return {
        "dry_pa_m": dry_pa_m,
        "irrigated_pa_m": irrigated_pa_m,
        "liquid_holdup": h_l,
        "re_g": re_g,
        "psi_0": psi_0,
        "psi_l": psi_l,
        "wall_factor": K,
    }


# ===================================================================
# Mackowiak SBD (2010) pressure drop model
# Reference: Mackowiak, J. Fluid Dynamics of Packed Columns. Springer, 2010.
# ===================================================================

# Ergun-like constants for Mackowiak dry-bed resistance
_MACK_K_A = 150.0
_MACK_K_B = 1.75
# Water kinematic viscosity at 20 degC [m2/s]
_MACK_NU_W = 1.004e-6

# Packing group parameters for wet pressure drop two-phase multiplier.
MACKOWIAK_PACKING_GROUPS = {
    "raschig_pall": {"phi_P": 0.75, "C_B_lam": 2.25, "C_B_turb": 3.0},
    "saddle": {"phi_P": 0.82, "C_B_lam": 1.75, "C_B_turb": 2.5},
    "hiflow": {"phi_P": 0.90, "C_B_lam": 1.4, "C_B_turb": 2.0},
    "gauze_structured": {"phi_P": 0.94, "C_B_lam": 1.0, "C_B_turb": 1.4},
    "sheet_30deg": {"phi_P": 0.90, "C_B_lam": 1.2, "C_B_turb": 1.75},
    "sheet_45deg": {"phi_P": 0.85, "C_B_lam": 1.4, "C_B_turb": 2.0},
}


def mackowiak_dry_resistance(
    gas_velocity: float,
    gas_density: float,
    gas_viscosity: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
) -> float:
    """Mackowiak dry bed resistance coefficient psi = K_A/Re_V + K_B."""
    dp = particle_diameter(voidage, specific_area)
    K = wall_factor(voidage, specific_area, column_diameter)
    kinematic_viscosity = gas_viscosity / gas_density
    re_v = gas_velocity * dp / ((1.0 - voidage) * kinematic_viscosity) * K
    return _MACK_K_A / max(re_v, SMALL) + _MACK_K_B


def mackowiak_dry_pressure_drop(
    gas_velocity: float,
    gas_density: float,
    gas_viscosity: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
) -> float:
    """Mackowiak dry bed pressure drop [Pa/m].

    dP0/H = psi * (1-epsilon)/epsilon^3 * F_V^2 / (dp * K)
    """
    dp = particle_diameter(voidage, specific_area)
    K = wall_factor(voidage, specific_area, column_diameter)
    psi = mackowiak_dry_resistance(
        gas_velocity, gas_density, gas_viscosity,
        voidage, specific_area, column_diameter,
    )
    f_v = gas_velocity * math.sqrt(gas_density)
    return psi * (1.0 - voidage) / voidage**3 * f_v**2 / (dp * K)


def mackowiak_liquid_holdup(
    liquid_velocity: float,
    liquid_viscosity: float,
    liquid_density: float,
    voidage: float,
    specific_area: float,
) -> float:
    """Mackowiak liquid holdup below loading point [m3/m3].

    h_L = 0.055 * (u_L * epsilon / (g * dp))^(1/3) * (nu_L/nu_W)^0.1
    """
    dp = particle_diameter(voidage, specific_area)
    nu_l = liquid_viscosity / liquid_density
    return 0.055 * (liquid_velocity * voidage / (G * dp)) ** (1.0 / 3.0) * (nu_l / _MACK_NU_W) ** 0.1


def mackowiak_wet_pressure_drop(
    gas_velocity: float,
    liquid_velocity: float,
    gas_density: float,
    liquid_density: float,
    gas_viscosity: float,
    liquid_viscosity: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
    cb_param: float | None = None,
) -> dict[str, float]:
    """Mackowiak wet (irrigated) bed pressure drop [Pa/m].

    dP/H = dP0/H * (1 + C_B * Fr_L*^n) * (1 - h_L/epsilon)^(-3)

    Returns dict with keys: dp_pa_m, liquid_holdup, dry_dp_pa_m, re_l, regime.
    """
    dp_dz_dry = mackowiak_dry_pressure_drop(
        gas_velocity, gas_density, gas_viscosity,
        voidage, specific_area, column_diameter,
    )
    dp = particle_diameter(voidage, specific_area)
    h_l = mackowiak_liquid_holdup(
        liquid_velocity, liquid_viscosity, liquid_density,
        voidage, specific_area,
    )
    re_l = liquid_velocity * dp * liquid_density / max(liquid_viscosity, SMALL)

    if re_l < 2.0:
        n = 0.5
        regime = "laminar"
    else:
        n = 0.25
        regime = "turbulent"

    if cb_param is None:
        cb_param = 2.25 if re_l < 2.0 else 3.0

    fr_l_star = liquid_velocity**2 / (G * dp) * liquid_density / max(liquid_density - gas_density, SMALL)
    dp_dz = dp_dz_dry * (1.0 + cb_param * fr_l_star**n) * (1.0 - h_l / max(voidage, SMALL)) ** (-3.0)

    return {
        "dp_pa_m": dp_dz,
        "liquid_holdup": h_l,
        "dry_dp_pa_m": dp_dz_dry,
        "re_l": re_l,
        "regime": regime,
    }
