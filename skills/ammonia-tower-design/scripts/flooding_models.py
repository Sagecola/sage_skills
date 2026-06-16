"""Flooding velocity correlations for packed towers.

This module collects all flooding velocity models:
- Blackwell-Kessler-Wankat (Kessler-Wankat log fit)
- Kister GPDC (Equations 2-6)
- Bain-Hougen (1944, two-constant)
- Mackowiak SBD (2010, suspended bed of droplets)

For pressure drop correlations, see pressure_drop_models.py.
"""

from __future__ import annotations

import math

try:
    from ._shared import (
        SMALL,
        G,
        G_FT_S2,
        FT_PER_M,
        LB_PER_KG,
        CP_PER_PA_S,
        TowerHydraulics,
        diameter_from_flow,
        gas_molar_volume_m3_per_kmol,
    )
    from .pressure_drop_models import (
        blackwell_abscissa,
        blackwell_pressure_drop_from_x,
        in_h2o_ft_to_pa_m,
        KISTER_GPDC_CONSTANTS,
        particle_diameter,
        mackowiak_dry_resistance,
    )
except ImportError:
    from _shared import (  # type: ignore[no-redef]
        SMALL,
        G,
        G_FT_S2,
        FT_PER_M,
        LB_PER_KG,
        CP_PER_PA_S,
        TowerHydraulics,
        diameter_from_flow,
        gas_molar_volume_m3_per_kmol,
    )
    from pressure_drop_models import (  # type: ignore[no-redef]
        blackwell_abscissa,
        blackwell_pressure_drop_from_x,
        in_h2o_ft_to_pa_m,
        KISTER_GPDC_CONSTANTS,
        particle_diameter,
        mackowiak_dry_resistance,
    )


def blackwell_flooding_ordinate(x_value: float) -> float:
    """Calculate flooding ordinate using Kessler-Wankat model.
    log(Y_f) = -1.6678 - 1.085 * log(X_f) - 0.29655 * (log(X_f))^2
    """
    log_x = math.log10(max(x_value, 1e-10))
    log_y = -1.6678 - 1.085 * log_x - 0.29655 * (log_x ** 2)
    return 10 ** log_y


def blackwell_velocity_from_ordinate(
    ordinate: float,
    packing_factor_ft_inv: float,
    gas_density_lb_ft3: float,
    liquid_density_lb_ft3: float,
    liquid_viscosity_cp: float,
    density_correction: float,
) -> float:
    """Calculate gas velocity from Blackwell ordinate.
    G_1 = { [Y * rho_G * (rho_L - rho_G) * g] / [F_p * mu_L^0.1] }^0.5
    """
    numerator = ordinate * gas_density_lb_ft3 * (liquid_density_lb_ft3 - gas_density_lb_ft3) * G_FT_S2
    denominator = packing_factor_ft_inv * (liquid_viscosity_cp ** 0.1) * density_correction
    g1 = math.sqrt(max(numerator / max(denominator, SMALL), 0.0))
    velocity_ft_s = g1 / max(gas_density_lb_ft3, SMALL)
    return velocity_ft_s / FT_PER_M


def kister_gpdc_flooding_velocity(
    *,
    packing_factor_ft_inv: float,
    flow_parameter: float,
    gas_density_lb_ft3: float,
    liquid_density_lb_ft3: float,
    kinematic_viscosity_cst: float,
    packing_type: str = "random",
) -> float:
    """Calculate flooding velocity using Kister GPDC method (Equations 2-6).

    Step 1: ΔP_fl/H = 0.12 * Fp^0.7
    Step 2: CP_fl = C1*(ΔP_fl/H)^C2 * [1-exp(C6*F_lv^C7)] / [1+C3*(ΔP_fl/H)^(C2/C4)*F_lv^C5]^C4
    Step 3: C_s,fl = CP_fl / (Fp^0.5 * ν^0.05)
    Step 4: u_s,fl = C_s,fl / sqrt(ρ_G / (ρ_L - ρ_G))
    """
    C1, C2, C3, C4, C5, C6, C7 = KISTER_GPDC_CONSTANTS[packing_type]

    dp_fl = 0.12 * (packing_factor_ft_inv ** 0.7)
    dp_term = dp_fl
    numerator = C1 * (dp_term ** C2) * (1.0 - math.exp(C6 * (flow_parameter ** C7)))
    denominator = (1.0 + C3 * (dp_term ** (C2 / C4)) * (flow_parameter ** C5)) ** C4
    cp_fl = numerator / max(denominator, SMALL)

    c_s_fl = cp_fl / max((packing_factor_ft_inv ** 0.5) * (kinematic_viscosity_cst ** 0.05), SMALL)

    density_ratio = gas_density_lb_ft3 / max(liquid_density_lb_ft3 - gas_density_lb_ft3, SMALL)
    velocity_ft_s = c_s_fl / math.sqrt(max(density_ratio, SMALL))

    return velocity_ft_s / FT_PER_M


def convert_to_imperial(
    liquid_flow_m3_h: float,
    gas_flow_m3_h: float,
    liquid_density_kg_m3: float,
    gas_density_kg_m3: float,
    liquid_viscosity_pa_s: float,
    packing_factor_m_inv: float,
) -> tuple[float, float, float, float, float, float]:
    """Convert SI units to imperial units for Blackwell/Kister correlations."""
    liquid_mass_flow_kg_h = liquid_density_kg_m3 * liquid_flow_m3_h
    gas_mass_flow_kg_h = gas_density_kg_m3 * gas_flow_m3_h

    liquid_mass_flow_lb_h = liquid_mass_flow_kg_h * LB_PER_KG
    gas_mass_flow_lb_h = gas_mass_flow_kg_h * LB_PER_KG
    liquid_density_lb_ft3 = liquid_density_kg_m3 * 0.06243
    gas_density_lb_ft3 = gas_density_kg_m3 * 0.06243
    liquid_viscosity_cp = liquid_viscosity_pa_s * CP_PER_PA_S
    packing_factor_ft_inv = packing_factor_m_inv * FT_PER_M

    return (
        liquid_mass_flow_lb_h,
        gas_mass_flow_lb_h,
        liquid_density_lb_ft3,
        gas_density_lb_ft3,
        liquid_viscosity_cp,
        packing_factor_ft_inv,
    )


def eckert_chart_fit_hydraulics(
    *,
    gas_flow_m3_h: float,
    liquid_flow_m3_h: float,
    packing_specific_area_m2_m3: float,
    min_wetting_rate_m3_m_h: float,
    operating_pressure_drop_in_h2o_ft: float,
    flooding_pressure_drop_in_h2o_ft: float,
    pressure_drop_packing_factor_m_inv: float,
    flooding_packing_factor_m_inv: float,
    density_correction: float,
    liquid_density_kg_m3: float,
    gas_density_kg_m3: float,
    liquid_viscosity_pa_s: float,
    flooding_method: str = "blackwell",
    packing_type: str = "random",
    # Mackowiak-specific parameters
    packing_voidage: float | None = None,
    column_diameter_m: float | None = None,
    surface_tension_n_m: float = 0.07275,
) -> tuple[TowerHydraulics, float, float, float]:
    liquid_mass_flow = liquid_density_kg_m3 * liquid_flow_m3_h
    gas_mass_flow = gas_density_kg_m3 * gas_flow_m3_h

    x_value = blackwell_abscissa(liquid_mass_flow, gas_mass_flow, liquid_density_kg_m3, gas_density_kg_m3)

    (
        liquid_mass_flow_lb_h,
        gas_mass_flow_lb_h,
        liquid_density_lb_ft3,
        gas_density_lb_ft3,
        liquid_viscosity_cp,
        packing_factor_ft_inv,
    ) = convert_to_imperial(
        liquid_flow_m3_h,
        gas_flow_m3_h,
        liquid_density_kg_m3,
        gas_density_kg_m3,
        liquid_viscosity_pa_s,
        pressure_drop_packing_factor_m_inv,
    )

    flood_ordinate = None

    if flooding_method == "kister":
        flow_parameter = (liquid_mass_flow_lb_h / max(gas_mass_flow_lb_h, SMALL)) * (
            (gas_density_lb_ft3 / max(liquid_density_lb_ft3, SMALL)) ** 0.5
        )
        kinematic_viscosity_cst = liquid_viscosity_cp
        flooding_velocity = kister_gpdc_flooding_velocity(
            packing_factor_ft_inv=packing_factor_ft_inv,
            flow_parameter=flow_parameter,
            gas_density_lb_ft3=gas_density_lb_ft3,
            liquid_density_lb_ft3=liquid_density_lb_ft3,
            kinematic_viscosity_cst=kinematic_viscosity_cst,
            packing_type=packing_type,
        )
    elif flooding_method == "mackowiak":
        if packing_voidage is None or column_diameter_m is None:
            raise ValueError(
                "Mackowiak method requires packing_voidage and column_diameter_m"
            )
        result = mackowiak_flooding_velocity(
            gas_density=gas_density_kg_m3,
            liquid_density=liquid_density_kg_m3,
            liquid_viscosity=liquid_viscosity_pa_s,
            surface_tension_n_m=surface_tension_n_m,
            voidage=packing_voidage,
            specific_area=packing_specific_area_m2_m3,
            column_diameter=column_diameter_m,
            liquid_mass_flow_kg_h=liquid_mass_flow,
            gas_mass_flow_kg_h=gas_mass_flow,
        )
        flooding_velocity = result["u_v_fl"]
    else:
        # Blackwell-Kessler-Wankat (default)
        flood_ordinate = blackwell_flooding_ordinate(x_value)
        flooding_velocity = blackwell_velocity_from_ordinate(
            flood_ordinate,
            packing_factor_ft_inv,
            gas_density_lb_ft3,
            liquid_density_lb_ft3,
            liquid_viscosity_cp,
            density_correction,
        )

    # Calculate operating pressure drop ordinate (always uses Blackwell polynomial)
    operating_ordinate = blackwell_pressure_drop_from_x(x_value, operating_pressure_drop_in_h2o_ft)

    # Calculate operating velocity from operating ordinate
    operating_velocity = blackwell_velocity_from_ordinate(
        operating_ordinate,
        packing_factor_ft_inv,
        gas_density_lb_ft3,
        liquid_density_lb_ft3,
        liquid_viscosity_cp,
        density_correction,
    )

    pressure_drop_pa_m = in_h2o_ft_to_pa_m(operating_pressure_drop_in_h2o_ft)

    diameter_m, area_m2 = diameter_from_flow(gas_flow_m3_h, operating_velocity)
    spray_density = liquid_flow_m3_h / area_m2
    min_spray_density = min_wetting_rate_m3_m_h * packing_specific_area_m2_m3
    min_liquid_flow = min_spray_density * area_m2

    hydraulics = TowerHydraulics(
        gas_flow_m3_h=gas_flow_m3_h,
        liquid_flow_m3_h=liquid_flow_m3_h,
        operating_velocity_m_s=operating_velocity,
        flooding_velocity_m_s=flooding_velocity,
        flooding_fraction=operating_velocity / max(flooding_velocity, SMALL),
        cross_section_m2=area_m2,
        tower_diameter_m=diameter_m,
        pressure_drop_pa_m=pressure_drop_pa_m,
        spray_density_m3_m2_h=spray_density,
        min_spray_density_m3_m2_h=min_spray_density,
        min_liquid_flow_m3_h=min_liquid_flow,
    )
    return hydraulics, x_value, operating_ordinate, flood_ordinate


# --- Bain-Hougen (1944) flooding velocity model ---


def bain_hougen_flooding_velocity(
    specific_area: float,
    voidage: float,
    gas_density: float,
    liquid_density: float,
    liquid_viscosity_mpa_s: float,
    liquid_mass_flow: float,
    gas_mass_flow: float,
    A: float,
    K: float = 1.75,
) -> float:
    """Calculate flooding velocity using Bain-Hougen correlation.

    Formula:
        log10[ u_F^2 / g * a / epsilon^3 * rho_G / rho_L * mu_L^0.2 ]
        = A - K * (L/G)^0.25 * (rho_G / rho_L)^0.125

    Solving for u_F:
        u_F = sqrt( g * epsilon^3 / a * rho_L / rho_G
                    * 10^(A - K * (L/G)^0.25 * (rho_G/rho_L)^0.125)
                    * mu_L^(-0.2) )
    """
    mass_flow_ratio = liquid_mass_flow / max(gas_mass_flow, 1e-12)
    density_ratio_term = (gas_density / liquid_density) ** 0.125
    flow_term = (mass_flow_ratio ** 0.25) * density_ratio_term
    exponent = A - K * flow_term

    return math.sqrt(
        G * (voidage ** 3) / specific_area
        * (liquid_density / gas_density)
        * (10.0 ** exponent)
        * (liquid_viscosity_mpa_s ** (-0.2))
    )


def bain_hougen_flooding_velocity_si(
    *,
    specific_area: float,
    voidage: float,
    gas_density: float,
    liquid_density: float,
    liquid_viscosity_pa_s: float,
    liquid_mass_flow_kg_h: float,
    gas_mass_flow_kg_h: float,
    A: float,
    K: float = 1.75,
) -> float:
    """Convenience wrapper with SI units (viscosity in Pa·s, flow in kg/h)."""
    liquid_viscosity_mpa_s = liquid_viscosity_pa_s * 1000.0
    return bain_hougen_flooding_velocity(
        specific_area=specific_area,
        voidage=voidage,
        gas_density=gas_density,
        liquid_density=liquid_density,
        liquid_viscosity_mpa_s=liquid_viscosity_mpa_s,
        liquid_mass_flow=liquid_mass_flow_kg_h,
        gas_mass_flow=gas_mass_flow_kg_h,
        A=A,
        K=K,
    )


# Packing-specific A constants database
BAIN_HOUGEN_CONSTANTS = {
    "ceramic raschig ring": {"A": 0.022, "K": 1.75},
    "ceramic intalox saddle": {"A": 0.176, "K": 1.75},
    "ceramic berl saddle": {"A": 0.26, "K": 1.75},
    "metal pall ring": {"A": 0.10, "K": 1.75},
    "metal cascade ring": {"A": 0.106, "K": 1.75},
    "metal imtp": {"A": 0.06225, "K": 1.75},
    "plastic pall ring": {"A": 0.0942, "K": 1.75},
    "plastic cascade ring": {"A": 0.204, "K": 1.75},
    "metal structured 250y": {"A": 0.291, "K": 1.75},
    "metal wire mesh": {"A": 0.30, "K": 1.75},
}


def get_bain_hougen_constant(packing_name: str) -> tuple[float, float] | None:
    """Get (A, K) constants for a named packing (lower-case English name)."""
    data = BAIN_HOUGEN_CONSTANTS.get(packing_name.lower().strip())
    if data:
        return data["A"], data["K"]
    return None


# ===================================================================
# Mackowiak SBD (2010) flooding velocity model
# Reference: Mackowiak, J. Fluid Dynamics of Packed Columns. Springer, 2010.
# ===================================================================


def mackowiak_flooding_velocity(
    *,
    gas_density: float,
    liquid_density: float,
    liquid_viscosity: float,
    surface_tension_n_m: float,
    voidage: float,
    specific_area: float,
    column_diameter: float,
    liquid_mass_flow_kg_h: float,
    gas_mass_flow_kg_h: float,
    channel_angle_deg: float = 0.0,
) -> dict[str, float]:
    """Mackowiak SBD flooding velocity [m/s].

    The flooding equation uses the dry resistance coefficient psi evaluated
    at a representative Reynolds number. The -1/6 exponent makes the result
    insensitive to errors in psi estimation.

    Args:
        channel_angle_deg: 0 for random packings, 30 for X-type structured, 45 for Y-type.

    Returns dict with keys: u_v_fl, h_l_fl0, psi_fl, d_t, d_h, lambda_0, k_rho_v.
    """
    alpha = math.radians(channel_angle_deg)
    delta_rho = liquid_density - gas_density

    d_t = math.sqrt(surface_tension_n_m / max(delta_rho * G, SMALL))
    d_h = 4.0 * voidage / specific_area
    lambda_0 = (liquid_mass_flow_kg_h / max(gas_mass_flow_kg_h, SMALL)) * (gas_density / liquid_density)

    dp = particle_diameter(voidage, specific_area)
    u_l_est = liquid_mass_flow_kg_h / max(liquid_density * 3600.0, SMALL)
    re_l_est = u_l_est * dp * liquid_density / max(liquid_viscosity, SMALL)

    if re_l_est < 2.0:
        m = -0.90 + lambda_0 / (lambda_0 + 0.5)
    else:
        m = -0.82 + lambda_0 / (lambda_0 + 0.5)

    discriminant = lambda_0**2 * (m + 2.0)**2 + 4.0 * lambda_0 * (m + 1.0) * (1.0 - lambda_0)
    if discriminant < 0.0:
        discriminant = 0.0
    h_l_fl0 = (math.sqrt(discriminant) - (m + 2.0) * lambda_0) / max(
        2.0 * (m + 1.0) * (1.0 - lambda_0), SMALL
    )
    h_l_fl0 = max(0.0, min(h_l_fl0, 0.99))

    psi_fl = mackowiak_dry_resistance(
        2.5, gas_density, 1.81e-5, voidage, specific_area, column_diameter,
    )

    if gas_density <= 1.165:
        k_rho_v = 1.0
    else:
        k_rho_v = (gas_density / 1.165) ** 0.18

    u_v_fl = (
        0.80
        * math.cos(alpha)
        * voidage ** (6.0 / 5.0)
        * psi_fl ** (-1.0 / 6.0)
        * math.sqrt(d_t * delta_rho * G / gas_density)
        * (d_h / max(d_t, SMALL)) ** (1.0 / 4.0)
        * (1.0 - h_l_fl0) ** (7.0 / 2.0)
        * k_rho_v
    )

    return {
        "u_v_fl": u_v_fl,
        "h_l_fl0": h_l_fl0,
        "psi_fl": psi_fl,
        "d_t": d_t,
        "d_h": d_h,
        "lambda_0": lambda_0,
        "k_rho_v": k_rho_v,
    }
