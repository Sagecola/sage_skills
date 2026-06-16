"""Preliminary calculation script for ammonia stripping and absorption towers.

This script supports a two-stage workflow:
1. Strip ammonia from wastewater into air.
2. Absorb ammonia from air into either water, hydrochloric acid, or both.

The stripper section follows the local project notes. The absorber section uses
the design-example framework: hydraulic sizing, wetting checks, Onda
correlations, and gas-phase NTU/HTU sizing. For HCl absorption, the mass
balance is reaction-based while the hydraulic and gas-film transfer framework is
kept consistent with the example approach.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    from ._shared import (
        SMALL,
        G,
        G_HOUR,
        PA_PER_IN_H2O,
        M_PER_FT,
        FT_PER_M,
        LB_PER_KG,
        CP_PER_PA_S,
        G_FT_S2,
        MW_N,
        MW_NH3,
        MW_H2O,
        MW_HCL,
        R_KPA_M3_PER_KMOL_K,
        P_ATM_KPA,
        TowerHydraulics,
        diameter_from_flow,
        suggested_nominal_diameter_m,
        gas_molar_volume_m3_per_kmol,
        pa_s_to_kg_m_h,
        dyn_cm_to_kg_h2,
    )
except ImportError:
    from _shared import (  # type: ignore[no-redef]
        SMALL,
        G,
        G_HOUR,
        PA_PER_IN_H2O,
        M_PER_FT,
        FT_PER_M,
        LB_PER_KG,
        CP_PER_PA_S,
        G_FT_S2,
        MW_N,
        MW_NH3,
        MW_H2O,
        MW_HCL,
        R_KPA_M3_PER_KMOL_K,
        P_ATM_KPA,
        TowerHydraulics,
        diameter_from_flow,
        suggested_nominal_diameter_m,
        gas_molar_volume_m3_per_kmol,
        pa_s_to_kg_m_h,
        dyn_cm_to_kg_h2,
    )


# --- Calculation-specific dataclasses ---


@dataclass
class StripperPackingResults:
    name: str
    role: str
    nominal_size: str
    packing_specific_area_m2_m3: float
    packing_factor_m_inv: float
    shape_factor: float
    critical_surface_tension_dyn_cm: float
    flooding_basis: str
    gpdc_abscissa: float
    operating_ordinate: float
    flooding_ordinate: float | None
    flooding_density_correction: float | None
    wet_area_fraction: float
    wet_packing_area_m2_m3: float
    gas_film_kga_kmol_m3_h_kpa: float
    liquid_film_kla_per_h: float
    overall_kga_kmol_m3_h_kpa: float
    gas_phase_htu_m: float
    overall_liquid_htu_m: float
    theoretical_packing_height_m: float
    design_packing_height_m: float
    hydraulics: TowerHydraulics
    warnings: list[str]


@dataclass
class StrippingResults:
    free_nh3_fraction: float
    influent_nh3_mg_l: float
    effluent_nh3_mg_l: float
    influent_liquid_mole_fraction: float
    effluent_liquid_mole_fraction: float
    equilibrium_slope: float
    equilibrium_exit_gas_mole_fraction: float
    minimum_molar_gas_liquid_ratio: float
    actual_molar_gas_liquid_ratio: float
    water_molar_flow_kmol_h: float
    air_molar_flow_kmol_h: float
    air_flow_m3_h: float
    gas_liquid_volume_ratio: float
    outlet_gas_mole_fraction: float
    outlet_gas_ppmv: float
    removal_fraction: float
    removed_n_kg_h: float
    removed_nh3_kg_h: float
    stripping_factor: float
    overall_liquid_ntu: float
    overall_liquid_htu_m: float
    theoretical_packing_height_m: float
    design_packing_height_m: float
    hydraulics: TowerHydraulics
    selected_packing: StripperPackingResults
    comparison_packings: list[StripperPackingResults]
    warnings: list[str]


@dataclass
class AbsorptionResults:
    mode: str
    inlet_nh3_mole_fraction: float
    outlet_nh3_mole_fraction: float
    outlet_nh3_ppmv: float
    capture_efficiency: float
    total_gas_molar_flow_kmol_h: float
    inlet_nh3_kmol_h: float
    captured_nh3_kmol_h: float
    captured_nh3_kg_h: float
    fresh_liquid_flow_m3_h: float
    recycle_liquid_flow_m3_h: float
    total_liquid_flow_m3_h: float
    minimum_liquid_gas_ratio: float | None
    actual_liquid_gas_ratio: float | None
    equilibrium_slope: float | None
    liquid_inlet_mole_fraction: float | None
    liquid_outlet_mole_fraction: float | None
    pure_hcl_kg_h: float | None
    acid_solution_kg_h: float | None
    acid_solution_m3_h: float | None
    wet_area_fraction: float
    wet_packing_area_m2_m3: float
    gas_film_kga_kmol_m3_h_kpa: float
    liquid_film_kla_per_h: float
    overall_kga_kmol_m3_h_kpa: float
    gas_phase_ntu: float
    gas_phase_htu_m: float
    theoretical_packing_height_m: float
    design_packing_height_m: float
    hydraulics: TowerHydraulics
    warnings: list[str]


@dataclass
class TwoStageResults:
    case_name: str | None
    stripping: StrippingResults
    absorptions: list[AbsorptionResults]


def ammonium_pka(temperature_c: float) -> float:
    temperature_k = temperature_c + 273.15
    return 0.09018 + 2729.92 / temperature_k


def free_ammonia_fraction(ph: float, temperature_c: float) -> float:
    pka = ammonium_pka(temperature_c)
    return 1.0 / (1.0 + 10.0 ** (pka - ph))


def ammonia_mg_l_as_n_to_nh3_mg_l(tan_mg_l_as_n: float, free_fraction: float) -> float:
    return tan_mg_l_as_n * free_fraction * MW_NH3 / MW_N


def liquid_mole_fraction_from_nh3_mg_l(nh3_mg_l: float) -> float:
    nh3_moles_per_l = nh3_mg_l / 1000.0 / MW_NH3
    water_moles_per_l = 1000.0 / MW_H2O
    return nh3_moles_per_l / (nh3_moles_per_l + water_moles_per_l)


def stripping_ntu(
    x_in: float,
    x_out: float,
    y_in: float,
    equilibrium_slope: float,
    stripping_factor: float,
) -> float:
    if math.isclose(stripping_factor, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        numerator = x_in - y_in / equilibrium_slope
        denominator = x_out - y_in / equilibrium_slope
        return numerator / denominator - 1.0

    ratio_term = ((1.0 - stripping_factor) * (x_in - y_in / equilibrium_slope)) / (
        x_out - y_in / equilibrium_slope
    )
    return math.log(ratio_term + stripping_factor) / (1.0 - stripping_factor)


def absorber_ntu_linear(
    y_in: float,
    y_out: float,
    x_in: float,
    equilibrium_slope: float,
    liquid_gas_ratio: float,
) -> float:
    factor = equilibrium_slope / liquid_gas_ratio
    bottom_driving_force = y_out - equilibrium_slope * x_in
    if bottom_driving_force <= 0.0:
        raise ValueError("Absorber operating line reaches equilibrium at the bottom; increase L/G.")
    if math.isclose(factor, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        return (y_in - y_out) / bottom_driving_force
    term = (1.0 - factor) * ((y_in - equilibrium_slope * x_in) / bottom_driving_force) + factor
    return math.log(term) / (1.0 - factor)


def gas_phase_ntu_reactive(y_in: float, y_out: float) -> float:
    return math.log(y_in / y_out)


def total_gas_molar_flow(stripping: StrippingResults) -> float:
    return stripping.air_molar_flow_kmol_h / max(1.0 - stripping.outlet_gas_mole_fraction, SMALL)


def henry_inverse_from_slope(
    equilibrium_slope: float,
    pressure_kpa: float,
    liquid_density_kg_m3: float,
) -> float:
    return liquid_density_kg_m3 / (equilibrium_slope * pressure_kpa * MW_H2O)



# Pressure drop and flooding correlations
try:
    from .pressure_drop_models import (
        blackwell_abscissa, blackwell_pressure_drop_from_x,
        in_h2o_ft_to_pa_m,
    )
    from .flooding_models import (
        blackwell_flooding_ordinate,
        blackwell_velocity_from_ordinate,
        kister_gpdc_flooding_velocity,
        convert_to_imperial,
        eckert_chart_fit_hydraulics,
    )
except ImportError:
    from pressure_drop_models import (  # type: ignore[no-redef]
        blackwell_abscissa, blackwell_pressure_drop_from_x,
        in_h2o_ft_to_pa_m,
    )
    from flooding_models import (  # type: ignore[no-redef]
        blackwell_flooding_ordinate,
        blackwell_velocity_from_ordinate,
        kister_gpdc_flooding_velocity,
        convert_to_imperial,
        eckert_chart_fit_hydraulics,
    )

def resolve_total_liquid_hydraulics(
    *,
    gas_flow_m3_h: float,
    fresh_liquid_flow_m3_h: float,
    specified_total_liquid_flow_m3_h: float | None,
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
    packing_voidage: float | None = None,
) -> tuple[float, TowerHydraulics]:
    trial_liquid_flow = max(fresh_liquid_flow_m3_h, specified_total_liquid_flow_m3_h or 0.0)
    provisional_hydraulics, _x_value, _operating_ordinate, _flood_ordinate = eckert_chart_fit_hydraulics(
        gas_flow_m3_h=gas_flow_m3_h,
        liquid_flow_m3_h=trial_liquid_flow,
        packing_specific_area_m2_m3=packing_specific_area_m2_m3,
        min_wetting_rate_m3_m_h=min_wetting_rate_m3_m_h,
        operating_pressure_drop_in_h2o_ft=operating_pressure_drop_in_h2o_ft,
        flooding_pressure_drop_in_h2o_ft=flooding_pressure_drop_in_h2o_ft,
        pressure_drop_packing_factor_m_inv=pressure_drop_packing_factor_m_inv,
        flooding_packing_factor_m_inv=flooding_packing_factor_m_inv,
        density_correction=density_correction,
        liquid_density_kg_m3=liquid_density_kg_m3,
        gas_density_kg_m3=gas_density_kg_m3,
        liquid_viscosity_pa_s=liquid_viscosity_pa_s,
        flooding_method=flooding_method,
        packing_type=packing_type,
        packing_voidage=packing_voidage,
        # Use initial diameter estimate; Mackowiak is insensitive to this
        column_diameter_m=0.5,
    )
    total_liquid_flow = max(trial_liquid_flow, provisional_hydraulics.min_liquid_flow_m3_h)
    hydraulics, _x_value, _operating_ordinate, _flood_ordinate = eckert_chart_fit_hydraulics(
        gas_flow_m3_h=gas_flow_m3_h,
        liquid_flow_m3_h=total_liquid_flow,
        packing_specific_area_m2_m3=packing_specific_area_m2_m3,
        min_wetting_rate_m3_m_h=min_wetting_rate_m3_m_h,
        operating_pressure_drop_in_h2o_ft=operating_pressure_drop_in_h2o_ft,
        flooding_pressure_drop_in_h2o_ft=flooding_pressure_drop_in_h2o_ft,
        pressure_drop_packing_factor_m_inv=pressure_drop_packing_factor_m_inv,
        flooding_packing_factor_m_inv=flooding_packing_factor_m_inv,
        density_correction=density_correction,
        liquid_density_kg_m3=liquid_density_kg_m3,
        gas_density_kg_m3=gas_density_kg_m3,
        liquid_viscosity_pa_s=liquid_viscosity_pa_s,
        flooding_method=flooding_method,
        packing_type=packing_type,
        packing_voidage=packing_voidage,
        column_diameter_m=0.5,
    )
    return total_liquid_flow, hydraulics


def packed_onda_coefficients(
    *,
    hydraulics: TowerHydraulics,
    total_gas_molar_flow_kmol_h: float,
    packing_area: float,
    liquid_density: float,
    gas_density: float,
    liquid_viscosity_pa_s: float,
    gas_viscosity_pa_s: float,
    liquid_diffusivity_m2_h: float,
    gas_diffusivity_m2_h: float,
    surface_tension_dyn_cm: float,
    critical_surface_tension_dyn_cm: float,
    shape_factor: float,
    temperature_c: float,
) -> dict[str, float]:
    area = hydraulics.cross_section_m2
    liquid_viscosity = pa_s_to_kg_m_h(liquid_viscosity_pa_s)
    gas_viscosity = pa_s_to_kg_m_h(gas_viscosity_pa_s)
    surface_tension = dyn_cm_to_kg_h2(surface_tension_dyn_cm)
    critical_surface_tension = dyn_cm_to_kg_h2(critical_surface_tension_dyn_cm)
    temperature_k = temperature_c + 273.15

    gas_mass_flux = gas_density * hydraulics.gas_flow_m3_h / area
    liquid_mass_flux = liquid_density * hydraulics.liquid_flow_m3_h / area

    wet_area_fraction = 1.0 - math.exp(
        -1.45
        * (critical_surface_tension / surface_tension) ** 0.75
        * (liquid_mass_flux / (packing_area * liquid_viscosity)) ** 0.1
        * ((liquid_mass_flux**2 * packing_area) / (liquid_density**2 * G_HOUR)) ** (-0.05)
        * ((liquid_mass_flux**2) / (liquid_density * surface_tension * packing_area)) ** 0.2
    )
    wet_area_fraction = min(max(wet_area_fraction, SMALL), 1.0)
    wet_packing_area = wet_area_fraction * packing_area

    gas_film_coefficient = (
        0.237
        * (gas_mass_flux / (packing_area * gas_viscosity)) ** 0.7
        * (gas_viscosity / (gas_density * gas_diffusivity_m2_h)) ** (1.0 / 3.0)
        * (packing_area * gas_diffusivity_m2_h / (R_KPA_M3_PER_KMOL_K * temperature_k))
    )
    liquid_film_coefficient = (
        0.0095
        # The local references disagree in OCR text, but the worked example
        # numbers and the stripping note both match the 2/3 Onda exponent.
        * (liquid_mass_flux / (wet_packing_area * liquid_viscosity)) ** (2.0 / 3.0)
        * (liquid_viscosity / (liquid_density * liquid_diffusivity_m2_h)) ** (-0.5)
        * (liquid_viscosity * G_HOUR / liquid_density) ** (1.0 / 3.0)
    )

    gas_film_kga = gas_film_coefficient * wet_packing_area * shape_factor**1.1
    liquid_film_kla = liquid_film_coefficient * wet_packing_area * shape_factor**0.4

    flooding_ratio = None
    if hydraulics.flooding_velocity_m_s is not None:
        flooding_ratio = hydraulics.operating_velocity_m_s / hydraulics.flooding_velocity_m_s

    corrected_gas_film_kga = gas_film_kga
    corrected_liquid_film_kla = liquid_film_kla
    if flooding_ratio is not None and flooding_ratio > 0.5:
        corrected_gas_film_kga = (
            1.0 + 9.5 * (flooding_ratio - 0.5) ** 1.4
        ) * gas_film_kga
        corrected_liquid_film_kla = (
            1.0 + 2.6 * (flooding_ratio - 0.5) ** 2.2
        ) * liquid_film_kla

    gas_molar_flux = total_gas_molar_flow_kmol_h / area

    return {
        "wet_area_fraction": wet_area_fraction,
        "wet_packing_area": wet_packing_area,
        "gas_mass_flux": gas_mass_flux,
        "liquid_mass_flux": liquid_mass_flux,
        "gas_film_kga": corrected_gas_film_kga,
        "liquid_film_kla": corrected_liquid_film_kla,
        "gas_molar_flux": gas_molar_flux,
        "flooding_ratio": flooding_ratio if flooding_ratio is not None else float("nan"),
    }


def onda_coefficients(
    args: argparse.Namespace,
    hydraulics: TowerHydraulics,
    total_gas_molar_flow_kmol_h: float,
) -> dict[str, float]:
    return packed_onda_coefficients(
        hydraulics=hydraulics,
        total_gas_molar_flow_kmol_h=total_gas_molar_flow_kmol_h,
        packing_area=args.absorber_packing_area,
        liquid_density=args.absorber_liquid_density,
        gas_density=args.absorber_gas_density,
        liquid_viscosity_pa_s=args.absorber_liquid_viscosity_pa_s,
        gas_viscosity_pa_s=args.absorber_gas_viscosity_pa_s,
        liquid_diffusivity_m2_h=args.absorber_liquid_diffusivity_m2_h,
        gas_diffusivity_m2_h=args.absorber_gas_diffusivity_m2_h,
        surface_tension_dyn_cm=args.absorber_surface_tension_dyn_cm,
        critical_surface_tension_dyn_cm=args.absorber_critical_surface_tension_dyn_cm,
        shape_factor=args.absorber_packing_shape_factor,
        temperature_c=args.temperature,
    )


def calculate_stripper_packing(
    args: argparse.Namespace,
    *,
    name: str,
    role: str,
    nominal_size: str,
    packing_area: float,
    min_wetting_rate: float,
    packing_factor: float,
    pressure_drop_packing_factor: float,
    shape_factor: float,
    critical_surface_tension_dyn_cm: float,
    flooding_density_correction: float | None,
    flooding_basis: str,
    ntu: float,
    stripping_factor: float,
    air_flow_m3_h: float,
    water_flow_m3_h: float,
    total_gas_flow_kmol_h: float,
    flooding_method: str = "blackwell",
    packing_type: str = "random",
    packing_voidage: float | None = None,
) -> StripperPackingResults:
    hydraulics, x_value, operating_ordinate, flood_ordinate = eckert_chart_fit_hydraulics(
        gas_flow_m3_h=air_flow_m3_h,
        liquid_flow_m3_h=water_flow_m3_h,
        packing_specific_area_m2_m3=packing_area,
        min_wetting_rate_m3_m_h=min_wetting_rate,
        operating_pressure_drop_in_h2o_ft=args.stripper_pressure_drop_in_h2o_ft,
        flooding_pressure_drop_in_h2o_ft=args.stripper_flooding_pressure_drop_in_h2o_ft,
        pressure_drop_packing_factor_m_inv=pressure_drop_packing_factor,
        flooding_packing_factor_m_inv=packing_factor,
        density_correction=flooding_density_correction or 1.0,
        liquid_density_kg_m3=args.stripper_liquid_density,
        gas_density_kg_m3=args.stripper_gas_density,
        liquid_viscosity_pa_s=args.stripper_liquid_viscosity_pa_s,
        flooding_method=flooding_method,
        packing_type=packing_type,
        packing_voidage=packing_voidage,
        column_diameter_m=0.5,
    )

    coeffs = packed_onda_coefficients(
        hydraulics=hydraulics,
        total_gas_molar_flow_kmol_h=total_gas_flow_kmol_h,
        packing_area=packing_area,
        liquid_density=args.stripper_liquid_density,
        gas_density=args.stripper_gas_density,
        liquid_viscosity_pa_s=args.stripper_liquid_viscosity_pa_s,
        gas_viscosity_pa_s=args.stripper_gas_viscosity_pa_s,
        liquid_diffusivity_m2_h=args.stripper_liquid_diffusivity_m2_h,
        gas_diffusivity_m2_h=args.stripper_gas_diffusivity_m2_h,
        surface_tension_dyn_cm=args.stripper_surface_tension_dyn_cm,
        critical_surface_tension_dyn_cm=critical_surface_tension_dyn_cm,
        shape_factor=shape_factor,
        temperature_c=args.temperature,
    )
    henry_inverse = henry_inverse_from_slope(
        args.stripper_equilibrium_slope,
        args.pressure,
        args.stripper_liquid_density,
    )
    overall_kga = 1.0 / (
        1.0 / coeffs["gas_film_kga"] + 1.0 / (henry_inverse * coeffs["liquid_film_kla"])
    )
    hog = coeffs["gas_molar_flux"] / (overall_kga * args.pressure)
    hol = stripping_factor * hog
    theoretical_height = ntu * hol
    design_height = theoretical_height * args.stripper_height_safety_factor

    warnings: list[str] = []
    if hydraulics.spray_density_m3_m2_h < hydraulics.min_spray_density_m3_m2_h:
        warnings.append(
            "Spray density is below the minimum wetting requirement; recirculation or a smaller diameter is needed."
        )
    if "Rosette" in name or "Taylor" in name:
        warnings.append(
            "Rosette ring (Taylor) shape factor and Cp0 are engineering estimates. Geometric data from HG/T 3986-2016 App. D."
        )
    warnings.append(
        "Hydraulics (operating point) computed with Blackwell pressure-drop correlation."
    )
    if hydraulics.flooding_velocity_m_s is not None:
        method_labels = {
            "blackwell": "Kessler-Wankat flooding correlation",
            "kister": "Kister GPDC flooding correlation",
            "mackowiak": "Mackowiak SBD flooding model",
        }
        label = method_labels.get(flooding_method, f"{flooding_method} flooding correlation")
        warnings.append(
            f"Flooding velocity was estimated using the {label}."
        )

    return StripperPackingResults(
        name=name,
        role=role,
        nominal_size=nominal_size,
        packing_specific_area_m2_m3=packing_area,
        packing_factor_m_inv=packing_factor,
        shape_factor=shape_factor,
        critical_surface_tension_dyn_cm=critical_surface_tension_dyn_cm,
        flooding_basis=flooding_basis,
        gpdc_abscissa=x_value,
        operating_ordinate=operating_ordinate,
        flooding_ordinate=flood_ordinate,
        flooding_density_correction=flooding_density_correction,
        wet_area_fraction=coeffs["wet_area_fraction"],
        wet_packing_area_m2_m3=coeffs["wet_packing_area"],
        gas_film_kga_kmol_m3_h_kpa=coeffs["gas_film_kga"],
        liquid_film_kla_per_h=coeffs["liquid_film_kla"],
        overall_kga_kmol_m3_h_kpa=overall_kga,
        gas_phase_htu_m=hog,
        overall_liquid_htu_m=hol,
        theoretical_packing_height_m=theoretical_height,
        design_packing_height_m=design_height,
        hydraulics=hydraulics,
        warnings=warnings,
    )


def calculate_stripping(args: argparse.Namespace) -> StrippingResults:
    effluent_tan = resolve_effluent_tan(args.influent_tan, args.effluent_tan, args.removal_fraction)
    if effluent_tan >= args.influent_tan:
        raise ValueError("Effluent TAN must be lower than influent TAN.")

    free_fraction = free_ammonia_fraction(args.ph, args.temperature)
    influent_nh3_mg_l = ammonia_mg_l_as_n_to_nh3_mg_l(args.influent_tan, free_fraction)
    effluent_nh3_mg_l = ammonia_mg_l_as_n_to_nh3_mg_l(effluent_tan, free_fraction)

    x_in = liquid_mole_fraction_from_nh3_mg_l(influent_nh3_mg_l)
    x_out = liquid_mole_fraction_from_nh3_mg_l(effluent_nh3_mg_l)
    y_in = args.stripper_gas_inlet_y
    y2_star = args.stripper_equilibrium_slope * x_in

    water_molar_flow = args.water_flow * 1000.0 / MW_H2O
    min_ratio = (x_in - x_out) / (y2_star - y_in)
    actual_ratio = args.stripper_design_factor * min_ratio
    air_molar_flow = actual_ratio * water_molar_flow
    air_flow_m3_h = air_molar_flow * gas_molar_volume_m3_per_kmol(args.temperature, args.pressure)
    gas_liquid_volume_ratio = air_flow_m3_h / args.water_flow
    y_out = y_in + (water_molar_flow / air_molar_flow) * (x_in - x_out)
    outlet_ppmv = y_out * 1e6

    removal_fraction = (args.influent_tan - effluent_tan) / args.influent_tan
    removed_n_kg_h = (args.influent_tan - effluent_tan) * args.water_flow / 1000.0
    removed_nh3_kg_h = removed_n_kg_h * MW_NH3 / MW_N

    stripping_factor = water_molar_flow / (air_molar_flow * args.stripper_equilibrium_slope)
    ntu = stripping_ntu(
        x_in,
        x_out,
        y_in,
        args.stripper_equilibrium_slope,
        stripping_factor,
    )

    total_gas_flow = air_molar_flow / max(1.0 - y_out, SMALL)

    main_packing = calculate_stripper_packing(
        args,
        name="PP Rosette ring (Taylor)",
        role="selected",
        nominal_size="DN73",
        packing_area=args.stripper_packing_area,
        min_wetting_rate=args.stripper_min_wetting_rate,
        packing_factor=args.stripper_main_packing_factor,
        pressure_drop_packing_factor=args.stripper_main_pressure_drop_packing_factor,
        shape_factor=args.stripper_main_shape_factor,
        critical_surface_tension_dyn_cm=args.stripper_main_critical_surface_tension_dyn_cm,
        flooding_density_correction=args.stripper_main_flooding_density_correction,
        flooding_basis="hydraulic calculation",
        ntu=ntu,
        stripping_factor=stripping_factor,
        air_flow_m3_h=air_flow_m3_h,
        water_flow_m3_h=args.water_flow,
        total_gas_flow_kmol_h=total_gas_flow,
        flooding_method=args.flooding_method,
        packing_type=args.packing_type,
        packing_voidage=0.89,  # Rosette ring DN73 per HG/T 3986-2016 App. D
    )
    comparison_packing = calculate_stripper_packing(
        args,
        name="PP Pall ring",
        role="comparison",
        nominal_size="DN50",
        packing_area=args.stripper_compare_packing_area,
        min_wetting_rate=args.stripper_compare_min_wetting_rate,
        packing_factor=args.stripper_compare_packing_factor,
        pressure_drop_packing_factor=args.stripper_compare_pressure_drop_packing_factor,
        shape_factor=args.stripper_compare_shape_factor,
        critical_surface_tension_dyn_cm=args.stripper_compare_critical_surface_tension_dyn_cm,
        flooding_density_correction=args.stripper_compare_flooding_density_correction,
        flooding_basis="hydraulic calculation",
        ntu=ntu,
        stripping_factor=stripping_factor,
        air_flow_m3_h=air_flow_m3_h,
        water_flow_m3_h=args.water_flow,
        total_gas_flow_kmol_h=total_gas_flow,
        flooding_method=args.flooding_method,
        packing_type=args.packing_type,
        packing_voidage=0.92,  # Pall ring DN50 per HG/T 3986-2016 App. A
    )

    warnings: list[str] = []
    if free_fraction < 0.95:
        warnings.append(
            "Free NH3 fraction is below 95%; pH or temperature may be insufficient for efficient stripping."
        )

    return StrippingResults(
        free_nh3_fraction=free_fraction,
        influent_nh3_mg_l=influent_nh3_mg_l,
        effluent_nh3_mg_l=effluent_nh3_mg_l,
        influent_liquid_mole_fraction=x_in,
        effluent_liquid_mole_fraction=x_out,
        equilibrium_slope=args.stripper_equilibrium_slope,
        equilibrium_exit_gas_mole_fraction=y2_star,
        minimum_molar_gas_liquid_ratio=min_ratio,
        actual_molar_gas_liquid_ratio=actual_ratio,
        water_molar_flow_kmol_h=water_molar_flow,
        air_molar_flow_kmol_h=air_molar_flow,
        air_flow_m3_h=air_flow_m3_h,
        gas_liquid_volume_ratio=gas_liquid_volume_ratio,
        outlet_gas_mole_fraction=y_out,
        outlet_gas_ppmv=outlet_ppmv,
        removal_fraction=removal_fraction,
        removed_n_kg_h=removed_n_kg_h,
        removed_nh3_kg_h=removed_nh3_kg_h,
        stripping_factor=stripping_factor,
        overall_liquid_ntu=ntu,
        overall_liquid_htu_m=main_packing.overall_liquid_htu_m,
        theoretical_packing_height_m=main_packing.theoretical_packing_height_m,
        design_packing_height_m=main_packing.design_packing_height_m,
        hydraulics=main_packing.hydraulics,
        selected_packing=main_packing,
        comparison_packings=[comparison_packing],
        warnings=warnings,
    )


def absorber_outlet_basis(args: argparse.Namespace, y_in: float) -> tuple[float, float]:
    if args.absorber_outlet_ppmv is not None:
        y_out = args.absorber_outlet_ppmv / 1e6
        if y_out >= y_in:
            raise ValueError("Absorber outlet ppmv must be lower than absorber inlet concentration.")
        capture_efficiency = 1.0 - y_out / y_in
        return y_out, capture_efficiency

    capture_efficiency = args.absorber_capture_efficiency
    return y_in * (1.0 - capture_efficiency), capture_efficiency


def calculate_water_absorption(args: argparse.Namespace, stripping: StrippingResults) -> AbsorptionResults:
    y_in = stripping.outlet_gas_mole_fraction
    y_out, capture_efficiency = absorber_outlet_basis(args, y_in)
    total_gas_flow = total_gas_molar_flow(stripping)
    x_in = args.absorber_water_inlet_x
    m = args.absorber_water_equilibrium_slope

    min_lg = (y_in - y_out) / ((y_in / m) - x_in)
    actual_lg = args.absorber_water_lg_factor * min_lg
    fresh_liquid_molar_flow = actual_lg * total_gas_flow
    fresh_liquid_flow = fresh_liquid_molar_flow * MW_H2O / args.absorber_liquid_density
    x_out = (y_in - y_out) / actual_lg + x_in

    total_liquid_flow, hydraulics = resolve_total_liquid_hydraulics(
        gas_flow_m3_h=stripping.air_flow_m3_h,
        fresh_liquid_flow_m3_h=fresh_liquid_flow,
        specified_total_liquid_flow_m3_h=args.absorber_total_liquid_flow,
        packing_specific_area_m2_m3=args.absorber_packing_area,
        min_wetting_rate_m3_m_h=args.absorber_min_wetting_rate,
        operating_pressure_drop_in_h2o_ft=args.absorber_pressure_drop_in_h2o_ft,
        flooding_pressure_drop_in_h2o_ft=args.absorber_flooding_pressure_drop_in_h2o_ft,
        pressure_drop_packing_factor_m_inv=args.absorber_pressure_drop_packing_factor,
        flooding_packing_factor_m_inv=args.absorber_flooding_packing_factor,
        density_correction=1.0,
        liquid_density_kg_m3=args.absorber_liquid_density,
        gas_density_kg_m3=args.absorber_gas_density,
        liquid_viscosity_pa_s=args.absorber_liquid_viscosity_pa_s,
        flooding_method=args.flooding_method,
        packing_type=args.packing_type,
        packing_voidage=0.92,  # Absorber Pall ring DN50 per HG/T 3986-2016 App. A
    )

    coeffs = onda_coefficients(args, hydraulics, total_gas_flow)
    overall_kga = 1.0 / (
        1.0 / coeffs["gas_film_kga"] + 1.0 / (args.absorber_henry_inverse * coeffs["liquid_film_kla"])
    )
    hog = coeffs["gas_molar_flux"] / (overall_kga * args.pressure)
    ntu = absorber_ntu_linear(y_in, y_out, x_in, m, actual_lg)
    theoretical_height = ntu * hog
    design_height = theoretical_height * args.absorber_height_safety_factor

    inlet_nh3_kmol_h = total_gas_flow * y_in
    captured_nh3_kmol_h = total_gas_flow * (y_in - y_out)

    warnings: list[str] = []
    recycle_liquid_flow = max(total_liquid_flow - fresh_liquid_flow, 0.0)

    if fresh_liquid_flow < hydraulics.min_liquid_flow_m3_h:
        warnings.append(
            "Fresh water flow is below the minimum wetting requirement; circulation can satisfy hydraulics but changes the simple once-through absorption basis."
        )
    warnings.append(
        "Water absorber follows the design-example framework: linear equilibrium, minimum L/G basis, and Onda transfer correlations."
    )
    warnings.append(
        "Absorber hydraulics (operating point) computed with Blackwell pressure-drop correlation."
    )

    return AbsorptionResults(
        mode="water",
        inlet_nh3_mole_fraction=y_in,
        outlet_nh3_mole_fraction=y_out,
        outlet_nh3_ppmv=y_out * 1e6,
        capture_efficiency=capture_efficiency,
        total_gas_molar_flow_kmol_h=total_gas_flow,
        inlet_nh3_kmol_h=inlet_nh3_kmol_h,
        captured_nh3_kmol_h=captured_nh3_kmol_h,
        captured_nh3_kg_h=captured_nh3_kmol_h * MW_NH3,
        fresh_liquid_flow_m3_h=fresh_liquid_flow,
        recycle_liquid_flow_m3_h=recycle_liquid_flow,
        total_liquid_flow_m3_h=total_liquid_flow,
        minimum_liquid_gas_ratio=min_lg,
        actual_liquid_gas_ratio=actual_lg,
        equilibrium_slope=m,
        liquid_inlet_mole_fraction=x_in,
        liquid_outlet_mole_fraction=x_out,
        pure_hcl_kg_h=None,
        acid_solution_kg_h=None,
        acid_solution_m3_h=None,
        wet_area_fraction=coeffs["wet_area_fraction"],
        wet_packing_area_m2_m3=coeffs["wet_packing_area"],
        gas_film_kga_kmol_m3_h_kpa=coeffs["gas_film_kga"],
        liquid_film_kla_per_h=coeffs["liquid_film_kla"],
        overall_kga_kmol_m3_h_kpa=overall_kga,
        gas_phase_ntu=ntu,
        gas_phase_htu_m=hog,
        theoretical_packing_height_m=theoretical_height,
        design_packing_height_m=design_height,
        hydraulics=hydraulics,
        warnings=warnings,
    )


def calculate_hcl_absorption(args: argparse.Namespace, stripping: StrippingResults) -> AbsorptionResults:
    y_in = stripping.outlet_gas_mole_fraction
    y_out, capture_efficiency = absorber_outlet_basis(args, y_in)
    total_gas_flow = total_gas_molar_flow(stripping)
    inlet_nh3_kmol_h = total_gas_flow * y_in
    captured_nh3_kmol_h = total_gas_flow * (y_in - y_out)
    pure_hcl_kg_h = captured_nh3_kmol_h * MW_HCL * args.absorber_acid_excess_factor
    acid_solution_kg_h = pure_hcl_kg_h / args.absorber_acid_weight_fraction
    acid_solution_m3_h = acid_solution_kg_h / args.absorber_acid_solution_density

    total_liquid_flow, hydraulics = resolve_total_liquid_hydraulics(
        gas_flow_m3_h=stripping.air_flow_m3_h,
        fresh_liquid_flow_m3_h=acid_solution_m3_h,
        specified_total_liquid_flow_m3_h=args.absorber_total_liquid_flow,
        packing_specific_area_m2_m3=args.absorber_packing_area,
        min_wetting_rate_m3_m_h=args.absorber_min_wetting_rate,
        operating_pressure_drop_in_h2o_ft=args.absorber_pressure_drop_in_h2o_ft,
        flooding_pressure_drop_in_h2o_ft=args.absorber_flooding_pressure_drop_in_h2o_ft,
        pressure_drop_packing_factor_m_inv=args.absorber_pressure_drop_packing_factor,
        flooding_packing_factor_m_inv=args.absorber_flooding_packing_factor,
        density_correction=1.0,
        liquid_density_kg_m3=args.absorber_liquid_density,
        gas_density_kg_m3=args.absorber_gas_density,
        liquid_viscosity_pa_s=args.absorber_liquid_viscosity_pa_s,
        flooding_method=args.flooding_method,
        packing_type=args.packing_type,
        packing_voidage=0.92,  # Absorber Pall ring DN50 per HG/T 3986-2016 App. A
    )

    coeffs = onda_coefficients(args, hydraulics, total_gas_flow)
    overall_kga = coeffs["gas_film_kga"]
    hog = coeffs["gas_molar_flux"] / (overall_kga * args.pressure)
    ntu = gas_phase_ntu_reactive(y_in, y_out)
    theoretical_height = ntu * hog
    design_height = theoretical_height * args.absorber_height_safety_factor

    recycle_liquid_flow = max(total_liquid_flow - acid_solution_m3_h, 0.0)

    warnings: list[str] = []
    if acid_solution_m3_h < hydraulics.min_liquid_flow_m3_h:
        warnings.append(
            "Fresh acid solution is below the minimum wetting requirement; circulation is required for hydraulics."
        )
    warnings.append(
        "HCl absorber uses reaction stoichiometry for acid demand and treats the transfer as gas-film controlled with y*=0."
    )
    warnings.append(
        "Absorber hydraulics (operating point) computed with Blackwell pressure-drop correlation."
    )

    return AbsorptionResults(
        mode="hcl",
        inlet_nh3_mole_fraction=y_in,
        outlet_nh3_mole_fraction=y_out,
        outlet_nh3_ppmv=y_out * 1e6,
        capture_efficiency=capture_efficiency,
        total_gas_molar_flow_kmol_h=total_gas_flow,
        inlet_nh3_kmol_h=inlet_nh3_kmol_h,
        captured_nh3_kmol_h=captured_nh3_kmol_h,
        captured_nh3_kg_h=captured_nh3_kmol_h * MW_NH3,
        fresh_liquid_flow_m3_h=acid_solution_m3_h,
        recycle_liquid_flow_m3_h=recycle_liquid_flow,
        total_liquid_flow_m3_h=total_liquid_flow,
        minimum_liquid_gas_ratio=None,
        actual_liquid_gas_ratio=None,
        equilibrium_slope=None,
        liquid_inlet_mole_fraction=None,
        liquid_outlet_mole_fraction=None,
        pure_hcl_kg_h=pure_hcl_kg_h,
        acid_solution_kg_h=acid_solution_kg_h,
        acid_solution_m3_h=acid_solution_m3_h,
        wet_area_fraction=coeffs["wet_area_fraction"],
        wet_packing_area_m2_m3=coeffs["wet_packing_area"],
        gas_film_kga_kmol_m3_h_kpa=coeffs["gas_film_kga"],
        liquid_film_kla_per_h=coeffs["liquid_film_kla"],
        overall_kga_kmol_m3_h_kpa=overall_kga,
        gas_phase_ntu=ntu,
        gas_phase_htu_m=hog,
        theoretical_packing_height_m=theoretical_height,
        design_packing_height_m=design_height,
        hydraulics=hydraulics,
        warnings=warnings,
    )


def calculate_absorptions(args: argparse.Namespace, stripping: StrippingResults) -> list[AbsorptionResults]:
    if args.absorber_mode == "water":
        return [calculate_water_absorption(args, stripping)]
    if args.absorber_mode == "hcl":
        return [calculate_hcl_absorption(args, stripping)]
    return [
        calculate_water_absorption(args, stripping),
        calculate_hcl_absorption(args, stripping),
    ]


def resolve_effluent_tan(
    influent_tan_mg_l: float,
    effluent_tan_mg_l: float | None,
    removal_fraction: float | None,
) -> float:
    if effluent_tan_mg_l is not None:
        return effluent_tan_mg_l
    if removal_fraction is None:
        raise ValueError("Provide either effluent TAN or removal fraction.")
    return influent_tan_mg_l * (1.0 - removal_fraction)


def load_preset(preset_name: str) -> dict[str, Any]:
    """Load a JSON preset file or built-in preset name. Returns merged defaults."""
    import json as _json
    # Try as file path first, then as built-in name
    preset_path = Path(preset_name)
    if preset_path.exists():
        path = preset_path
    else:
        builtin = Path(__file__).resolve().parent.parent / "presets" / f"{preset_name}.json"
        if builtin.exists():
            path = builtin
        else:
            raise FileNotFoundError(f"Preset not found: {preset_name} (tried {preset_name} and {builtin})")
    with open(path, encoding="utf-8") as f:
        data = _json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def apply_presets(args: argparse.Namespace) -> argparse.Namespace:
    """Apply --preset and/or --case values as defaults. CLI args always override."""
    defaults: dict[str, Any] = {}

    # Load --preset if given
    if args.preset:
        defaults.update(load_preset(args.preset))

    # --case hanglian is shorthand for --preset hanglian
    if args.case == "hanglian" and not args.preset:
        defaults.update(load_preset("hanglian"))

    # Apply defaults only where CLI didn't set a value
    for key, value in defaults.items():
        if hasattr(args, key) and getattr(args, key) is None:
            setattr(args, key, value)
        elif not hasattr(args, key):
            setattr(args, key, value)

    return args



# Imported from split modules
try:
    from .cli_parser import build_parser, validate_args
    from .report_formatter import (
        format_hydraulics,
        format_stripper_packing,
        format_absorption,
        format_report,
        format_markdown_report,
        markdown_title,
    )
except ImportError:
    from cli_parser import build_parser, validate_args  # type: ignore[no-redef]
    from report_formatter import (  # type: ignore[no-redef]
        format_hydraulics,
        format_stripper_packing,
        format_absorption,
        format_report,
        format_markdown_report,
        markdown_title,
    )


def write_markdown_report(path_str: str, content: str) -> Path:
    path = Path(path_str)
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def resolve_markdown_output_path(args: argparse.Namespace, results: TwoStageResults) -> str | None:
    if args.write_markdown is None:
        return None
    if args.write_markdown != "__AUTO__":
        return args.write_markdown
    if results.case_name == "hanglian":
        return "自动生成-杭联示例.md"
    return "自动生成-两段塔设计计算.md"


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args = apply_presets(args)
    validate_args(args)

    stripping = calculate_stripping(args)
    absorptions = calculate_absorptions(args, stripping)
    results = TwoStageResults(case_name=args.case, stripping=stripping, absorptions=absorptions)

    if args.write_markdown is not None:
        md_content = format_markdown_report(args, results)
        md_path = resolve_markdown_output_path(args, results)
        if md_path is not None:
            write_markdown_report(md_path, md_content)
            print(f"Markdown report written to: {md_path}")

    if args.json:
        print(json.dumps(asdict(results), indent=2))
    else:
        print(format_report(results))


if __name__ == "__main__":
    main()
