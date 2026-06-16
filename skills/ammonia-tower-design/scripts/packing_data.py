"""Packing parameter database for Chinese standard and generic packings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PackingSpec:
    name: str
    material: str
    nominal_size_mm: float
    specific_area_m2_m3: float
    void_fraction: float
    packing_factor_m_inv: Optional[float]
    shape_factor_onda: float
    critical_surface_tension_dyn_cm: float
    min_wetting_rate_m3_m_h: float
    billet_schultes_cp0: Optional[float] = None
    billet_schultes_CFl: Optional[float] = None
    billet_schultes_CS: Optional[float] = None
    billet_schultes_Ch: Optional[float] = None
    bain_hougen_A: Optional[float] = None
    mackowiak_group: str = "raschig_pall"
    source: str = ""
    notes: str = ""


HG_T_3986_PLASTIC_PACKINGS = [
    # ===================================================================
    # ALL data below is per HG/T 3986-2016 "塑料塔填料".
    # The standard covers PP (polypropylene) material only.
    # Bulk density values in the standard are calculated assuming
    # PP density = 900 kg/m3. For other plastics (PE, PVC, PVDF etc.)
    # the standard says to scale bulk density by material density ratio.
    # Geometric data (a, epsilon) and dry packing factor (phi) are from
    # the standard appendices. Shape factor, Cp0, and Bain-Hougen A
    # are engineering estimates — NOT from the standard.
    # ===================================================================

    # --- Plastic Pall Ring (鲍尔环) — HG/T 3986-2016 Appendix A ---
    # a, epsilon, and dry packing factor (phi) are from the standard.
    # Shape factor, Cp0, and Bain-Hougen A are engineering estimates.
    PackingSpec(
        name="PP Pall ring", material="PP", nominal_size_mm=16.0,
        specific_area_m2_m3=274.0, void_fraction=0.90, packing_factor_m_inv=376.0,
        shape_factor_onda=1.45, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.60,
        bain_hougen_A=0.0942,
        source="HG/T 3986-2016 App. A", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="PP Pall ring", material="PP", nominal_size_mm=25.0,
        specific_area_m2_m3=213.0, void_fraction=0.91, packing_factor_m_inv=283.0,
        shape_factor_onda=1.45, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=0.865, billet_schultes_CFl=2.064, billet_schultes_CS=2.696, billet_schultes_Ch=0.528,
        bain_hougen_A=0.0942,
        source="HG/T 3986-2016 App. A", notes="BS constants from Billet-Schultes 1999; psi, A are estimates",
    ),
    PackingSpec(
        name="PP Pall ring", material="PP", nominal_size_mm=38.0,
        specific_area_m2_m3=151.0, void_fraction=0.91, packing_factor_m_inv=200.0,
        shape_factor_onda=1.45, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.78,
        bain_hougen_A=0.0942,
        source="HG/T 3986-2016 App. A", notes="Cp0 interpolated from BS 1999; psi, A are estimates",
    ),
    PackingSpec(
        name="PP Pall ring", material="PP", nominal_size_mm=50.0,
        specific_area_m2_m3=100.0, void_fraction=0.92, packing_factor_m_inv=128.0,
        shape_factor_onda=1.45, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=0.698, billet_schultes_CFl=1.757, billet_schultes_CS=2.816, billet_schultes_Ch=0.593,
        bain_hougen_A=0.0942,
        source="HG/T 3986-2016 App. A", notes="BS constants from Billet-Schultes 1999; psi, A are estimates",
    ),
    PackingSpec(
        name="PP Pall ring", material="PP", nominal_size_mm=76.0,
        specific_area_m2_m3=72.0, void_fraction=0.92, packing_factor_m_inv=92.0,
        shape_factor_onda=1.45, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.60,
        bain_hougen_A=0.0942,
        source="HG/T 3986-2016 App. A", notes="Cp0 extrapolated from BS 1999; psi, A are estimates",
    ),

    # --- Plastic Cascade Ring (阶梯环) — HG/T 3986-2016 Appendix B ---
    PackingSpec(
        name="PP Cascade ring", material="PP", nominal_size_mm=16.0,
        specific_area_m2_m3=346.0, void_fraction=0.85, packing_factor_m_inv=563.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.50,
        bain_hougen_A=0.204,
        source="HG/T 3986-2016 App. B", notes="CMR; Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="PP Cascade ring", material="PP", nominal_size_mm=25.0,
        specific_area_m2_m3=214.0, void_fraction=0.91, packing_factor_m_inv=284.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.45,
        bain_hougen_A=0.204,
        source="HG/T 3986-2016 App. B", notes="CMR; Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="PP Cascade ring", material="PP", nominal_size_mm=38.0,
        specific_area_m2_m3=172.0, void_fraction=0.93, packing_factor_m_inv=214.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.40,
        bain_hougen_A=0.204,
        source="HG/T 3986-2016 App. B", notes="CMR; Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="PP Cascade ring", material="PP", nominal_size_mm=50.0,
        specific_area_m2_m3=121.0, void_fraction=0.93, packing_factor_m_inv=150.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.38,
        bain_hougen_A=0.204,
        source="HG/T 3986-2016 App. B", notes="CMR; Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="PP Cascade ring", material="PP", nominal_size_mm=76.0,
        specific_area_m2_m3=84.0, void_fraction=0.93, packing_factor_m_inv=104.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.35,
        bain_hougen_A=0.204,
        source="HG/T 3986-2016 App. B", notes="CMR; Cp0, psi, A are estimates",
    ),

    # --- Plastic Rosette Ring (花环) — HG/T 3986-2016 Appendix D ---
    PackingSpec(
        name="PP Rosette ring", material="PP", nominal_size_mm=25.0,
        specific_area_m2_m3=269.0, void_fraction=0.86, packing_factor_m_inv=423.0,
        shape_factor_onda=1.55, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.60,
        source="HG/T 3986-2016 App. D", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Rosette ring", material="PP", nominal_size_mm=47.0,
        specific_area_m2_m3=185.0, void_fraction=0.88, packing_factor_m_inv=271.0,
        shape_factor_onda=1.55, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.55,
        source="HG/T 3986-2016 App. D", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Rosette ring", material="PP", nominal_size_mm=51.0,
        specific_area_m2_m3=180.0, void_fraction=0.89, packing_factor_m_inv=255.0,
        shape_factor_onda=1.55, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.50,
        source="HG/T 3986-2016 App. D", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Rosette ring", material="PP", nominal_size_mm=59.0,
        specific_area_m2_m3=150.0, void_fraction=0.89, packing_factor_m_inv=213.0,
        shape_factor_onda=1.55, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.48,
        source="HG/T 3986-2016 App. D", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Rosette ring", material="PP", nominal_size_mm=73.0,
        specific_area_m2_m3=127.0, void_fraction=0.89, packing_factor_m_inv=180.0,
        shape_factor_onda=1.55, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=0.54, billet_schultes_CFl=2.13, billet_schultes_CS=2.91, billet_schultes_Ch=0.59,
        source="HG/T 3986-2016 App. D",
        notes="aka Taylor ring; BS constants from Tellerette 25mm in BS 1999; psi is estimate",
    ),
    PackingSpec(
        name="PP Rosette ring", material="PP", nominal_size_mm=95.0,
        specific_area_m2_m3=94.0, void_fraction=0.90, packing_factor_m_inv=129.0,
        shape_factor_onda=1.55, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.45,
        source="HG/T 3986-2016 App. D", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Rosette ring", material="PP", nominal_size_mm=145.0,
        specific_area_m2_m3=65.0, void_fraction=0.95, packing_factor_m_inv=76.0,
        shape_factor_onda=1.55, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.40,
        source="HG/T 3986-2016 App. D", notes="Cp0, psi are engineering estimates",
    ),

    # --- Plastic Conjugate Ring (共轭环) — HG/T 3986-2016 Appendix C ---
    PackingSpec(
        name="PP Conjugate ring", material="PP", nominal_size_mm=25.0,
        specific_area_m2_m3=185.0, void_fraction=0.90, packing_factor_m_inv=254.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.45,
        source="HG/T 3986-2016 App. C", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Conjugate ring", material="PP", nominal_size_mm=38.0,
        specific_area_m2_m3=142.0, void_fraction=0.91, packing_factor_m_inv=188.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.40,
        source="HG/T 3986-2016 App. C", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Conjugate ring", material="PP", nominal_size_mm=50.0,
        specific_area_m2_m3=104.0, void_fraction=0.92, packing_factor_m_inv=134.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.38,
        source="HG/T 3986-2016 App. C", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Conjugate ring", material="PP", nominal_size_mm=76.0,
        specific_area_m2_m3=81.0, void_fraction=0.93, packing_factor_m_inv=101.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.35,
        source="HG/T 3986-2016 App. C", notes="Cp0, psi are engineering estimates",
    ),

    # --- Plastic Intalox Saddle (矩鞍环) — HG/T 3986-2016 Appendix J ---
    PackingSpec(
        name="PP Intalox saddle", material="PP", nominal_size_mm=25.0,
        specific_area_m2_m3=258.0, void_fraction=0.89, packing_factor_m_inv=366.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.55,
        mackowiak_group="saddle",
        source="HG/T 3986-2016 App. J", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Intalox saddle", material="PP", nominal_size_mm=38.0,
        specific_area_m2_m3=170.0, void_fraction=0.91, packing_factor_m_inv=226.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.50,
        mackowiak_group="saddle",
        source="HG/T 3986-2016 App. J", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Intalox saddle", material="PP", nominal_size_mm=50.0,
        specific_area_m2_m3=120.0, void_fraction=0.92, packing_factor_m_inv=154.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.45,
        mackowiak_group="saddle",
        source="HG/T 3986-2016 App. J", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Intalox saddle", material="PP", nominal_size_mm=76.0,
        specific_area_m2_m3=105.0, void_fraction=0.93, packing_factor_m_inv=131.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.40,
        mackowiak_group="saddle",
        source="HG/T 3986-2016 App. J", notes="Cp0, psi are engineering estimates",
    ),

    # --- Plastic Hi-Flow Ring (海尔环) — HG/T 3986-2016 Appendix E ---
    PackingSpec(
        name="PP Hiflow ring", material="PP", nominal_size_mm=50.0,
        specific_area_m2_m3=107.0, void_fraction=0.93, packing_factor_m_inv=128.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.40,
        mackowiak_group="hiflow",
        source="HG/T 3986-2016 App. E", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Hiflow ring", material="PP", nominal_size_mm=76.0,
        specific_area_m2_m3=75.0, void_fraction=0.94, packing_factor_m_inv=87.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.35,
        mackowiak_group="hiflow",
        source="HG/T 3986-2016 App. E", notes="Cp0, psi are engineering estimates",
    ),
    PackingSpec(
        name="PP Hiflow ring", material="PP", nominal_size_mm=100.0,
        specific_area_m2_m3=55.0, void_fraction=0.95, packing_factor_m_inv=62.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.30,
        mackowiak_group="hiflow",
        source="HG/T 3986-2016 App. E", notes="Cp0, psi are engineering estimates",
    ),

    # --- Plastic Flat Ring (扁环) — HG/T 3986-2016 Appendix I ---
    PackingSpec(
        name="PP Flat ring", material="PP", nominal_size_mm=38.0,
        specific_area_m2_m3=145.0, void_fraction=0.92, packing_factor_m_inv=186.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.42,
        source="HG/T 3986-2016 App. I", notes="QH-type; Cp0, psi are estimates",
    ),
    PackingSpec(
        name="PP Flat ring", material="PP", nominal_size_mm=50.0,
        specific_area_m2_m3=128.0, void_fraction=0.93, packing_factor_m_inv=159.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.38,
        source="HG/T 3986-2016 App. I", notes="QH-type; Cp0, psi are estimates",
    ),
    PackingSpec(
        name="PP Flat ring", material="PP", nominal_size_mm=76.0,
        specific_area_m2_m3=116.0, void_fraction=0.93, packing_factor_m_inv=144.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.35,
        source="HG/T 3986-2016 App. I", notes="QH-type; Cp0, psi are estimates",
    ),
]

# ===================================================================
# Metal packings per HG/T 4374-2012 "金属塔填料技术条件"
# Data is for stainless steel (material density = 7850 kg/m3).
# Carbon steel walls may be 20-50% thicker; adjust parameters accordingly.
# Shape factor, Cp0, and Bain-Hougen A are engineering estimates.
# Critical surface tension = 75 dyn/cm for stainless steel.
# ===================================================================
HG_T_4374_METAL_RANDOM_PACKINGS = [
    # --- Metal Raschig Ring (拉西环) — HG/T 4374-2012 Appendix A ---
    PackingSpec(
        name="Metal Raschig ring", material="SS", nominal_size_mm=16.0,
        specific_area_m2_m3=338.0, void_fraction=0.94, packing_factor_m_inv=407.0,
        shape_factor_onda=1.75, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.20,
        bain_hougen_A=0.022,
        source="HG/T 4374-2012 App. A", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Raschig ring", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=184.0, void_fraction=0.95, packing_factor_m_inv=215.0,
        shape_factor_onda=1.75, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.10,
        bain_hougen_A=0.022,
        source="HG/T 4374-2012 App. A", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Raschig ring", material="SS", nominal_size_mm=38.0,
        specific_area_m2_m3=128.0, void_fraction=0.96, packing_factor_m_inv=145.0,
        shape_factor_onda=1.75, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.05,
        bain_hougen_A=0.022,
        source="HG/T 4374-2012 App. A", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Raschig ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=95.0, void_fraction=0.96, packing_factor_m_inv=107.0,
        shape_factor_onda=1.75, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.00,
        bain_hougen_A=0.022,
        source="HG/T 4374-2012 App. A", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Raschig ring", material="SS", nominal_size_mm=76.0,
        specific_area_m2_m3=66.0, void_fraction=0.97, packing_factor_m_inv=72.0,
        shape_factor_onda=1.75, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.90,
        bain_hougen_A=0.022,
        source="HG/T 4374-2012 App. A", notes="Cp0, psi, A are estimates",
    ),

    # --- Metal Pall Ring (鲍尔环) — HG/T 4374-2012 Appendix C ---
    PackingSpec(
        name="Metal Pall ring", material="SS", nominal_size_mm=16.0,
        specific_area_m2_m3=362.0, void_fraction=0.95, packing_factor_m_inv=423.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.45,
        bain_hougen_A=0.10,
        source="HG/T 4374-2012 App. C", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Pall ring", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=219.0, void_fraction=0.95, packing_factor_m_inv=255.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=0.957, billet_schultes_CFl=2.083, billet_schultes_CS=2.627, billet_schultes_Ch=0.719,
        bain_hougen_A=0.10,
        source="HG/T 4374-2012 App. C", notes="BS constants from Billet-Schultes 1999; psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Pall ring", material="SS", nominal_size_mm=38.0,
        specific_area_m2_m3=146.0, void_fraction=0.96, packing_factor_m_inv=165.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.85,
        bain_hougen_A=0.10,
        source="HG/T 4374-2012 App. C", notes="Cp0 interpolated from BS 1999; psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Pall ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=109.0, void_fraction=0.96, packing_factor_m_inv=124.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=0.763, billet_schultes_CFl=1.580, billet_schultes_CS=2.725, billet_schultes_Ch=0.784,
        bain_hougen_A=0.10,
        source="HG/T 4374-2012 App. C", notes="BS constants from Billet-Schultes 1999; psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Pall ring", material="SS", nominal_size_mm=76.0,
        specific_area_m2_m3=71.0, void_fraction=0.96, packing_factor_m_inv=80.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.65,
        bain_hougen_A=0.10,
        source="HG/T 4374-2012 App. C", notes="Cp0 extrapolated from BS 1999; psi, A are estimates",
    ),

    # --- Metal Cascade Ring (阶梯环 / CMR) — HG/T 4374-2012 Appendix D ---
    PackingSpec(
        name="Metal Cascade ring", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=221.0, void_fraction=0.95, packing_factor_m_inv=257.0,
        shape_factor_onda=1.35, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.42,
        bain_hougen_A=0.106,
        source="HG/T 4374-2012 App. D", notes="CMR; Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Cascade ring", material="SS", nominal_size_mm=38.0,
        specific_area_m2_m3=153.0, void_fraction=0.96, packing_factor_m_inv=173.0,
        shape_factor_onda=1.35, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.38,
        bain_hougen_A=0.106,
        source="HG/T 4374-2012 App. D", notes="CMR; Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Cascade ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=109.0, void_fraction=0.96, packing_factor_m_inv=123.0,
        shape_factor_onda=1.35, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.35,
        bain_hougen_A=0.106,
        source="HG/T 4374-2012 App. D", notes="CMR; Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal Cascade ring", material="SS", nominal_size_mm=76.0,
        specific_area_m2_m3=75.0, void_fraction=0.96, packing_factor_m_inv=85.0,
        shape_factor_onda=1.35, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.32,
        bain_hougen_A=0.106,
        source="HG/T 4374-2012 App. D", notes="CMR; Cp0, psi, A are estimates",
    ),

    # --- Metal IMTP (矩鞍环) — HG/T 4374-2012 Appendix B ---
    PackingSpec(
        name="Metal IMTP", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=185.0, void_fraction=0.96, packing_factor_m_inv=209.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.45,
        bain_hougen_A=0.06225,
        mackowiak_group="saddle",
        source="HG/T 4374-2012 App. B", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal IMTP", material="SS", nominal_size_mm=38.0,
        specific_area_m2_m3=112.0, void_fraction=0.96, packing_factor_m_inv=137.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.40,
        bain_hougen_A=0.06225,
        mackowiak_group="saddle",
        source="HG/T 4374-2012 App. B", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal IMTP", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=75.0, void_fraction=0.96, packing_factor_m_inv=85.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.35,
        bain_hougen_A=0.06225,
        mackowiak_group="saddle",
        source="HG/T 4374-2012 App. B", notes="Cp0, psi, A are estimates",
    ),
    PackingSpec(
        name="Metal IMTP", material="SS", nominal_size_mm=76.0,
        specific_area_m2_m3=58.0, void_fraction=0.97, packing_factor_m_inv=63.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.32,
        bain_hougen_A=0.06225,
        mackowiak_group="saddle",
        source="HG/T 4374-2012 App. B", notes="Cp0, psi, A are estimates",
    ),

    # --- Metal Conjugate Ring (共轭环) — HG/T 4374-2012 Appendix E ---
    PackingSpec(
        name="Metal Conjugate ring", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=185.0, void_fraction=0.95, packing_factor_m_inv=216.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.42,
        source="HG/T 4374-2012 App. E", notes="Cp0, psi are estimates",
    ),
    PackingSpec(
        name="Metal Conjugate ring", material="SS", nominal_size_mm=38.0,
        specific_area_m2_m3=116.0, void_fraction=0.96, packing_factor_m_inv=131.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.38,
        source="HG/T 4374-2012 App. E", notes="Cp0, psi are estimates",
    ),
    PackingSpec(
        name="Metal Conjugate ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=86.0, void_fraction=0.96, packing_factor_m_inv=97.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.35,
        source="HG/T 4374-2012 App. E", notes="Cp0, psi are estimates",
    ),

    # --- Metal Flat Ring (扁环 / QH) — HG/T 4374-2012 Appendix F ---
    PackingSpec(
        name="Metal Flat ring", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=228.0, void_fraction=0.94, packing_factor_m_inv=280.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.40,
        bain_hougen_A=0.0749,
        source="HG/T 4374-2012 App. F", notes="QH-type; Cp0, psi are estimates",
    ),
    PackingSpec(
        name="Metal Flat ring", material="SS", nominal_size_mm=38.0,
        specific_area_m2_m3=150.0, void_fraction=0.95, packing_factor_m_inv=175.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.35,
        bain_hougen_A=0.0749,
        source="HG/T 4374-2012 App. F", notes="QH-type; Cp0, psi are estimates",
    ),
    PackingSpec(
        name="Metal Flat ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=115.0, void_fraction=0.97, packing_factor_m_inv=156.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.32,
        bain_hougen_A=0.0749,
        source="HG/T 4374-2012 App. F", notes="QH-type; Cp0, psi are estimates",
    ),

    # --- Metal 八四内弧环 — HG/T 4374-2012 Appendix G ---
    PackingSpec(
        name="Metal BaSi ring", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=250.0, void_fraction=0.93, packing_factor_m_inv=310.0,
        shape_factor_onda=1.50, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.45,
        source="HG/T 4374-2012 App. G", notes="八四内弧环; Cp0, psi are estimates",
    ),
    PackingSpec(
        name="Metal BaSi ring", material="SS", nominal_size_mm=38.0,
        specific_area_m2_m3=138.0, void_fraction=0.95, packing_factor_m_inv=163.0,
        shape_factor_onda=1.50, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.40,
        source="HG/T 4374-2012 App. G", notes="八四内弧环; Cp0, psi are estimates",
    ),
    PackingSpec(
        name="Metal BaSi ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=121.0, void_fraction=0.95, packing_factor_m_inv=144.0,
        shape_factor_onda=1.50, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.35,
        source="HG/T 4374-2012 App. G", notes="八四内弧环; Cp0, psi are estimates",
    ),
    PackingSpec(
        name="Metal BaSi ring", material="SS", nominal_size_mm=76.0,
        specific_area_m2_m3=75.0, void_fraction=0.95, packing_factor_m_inv=86.0,
        shape_factor_onda=1.50, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.12, billet_schultes_cp0=0.32,
        source="HG/T 4374-2012 App. G", notes="八四内弧环; Cp0, psi are estimates",
    ),
]

# Metal structured packings per HG/T 4374-2012 Appendices H, I, J.
# The standard provides a (specific area) and epsilon. Packing factor is NOT
# specified for structured packings in this standard; use vendor data or
# Kister GPDC factors from Wolf-Zöllner 2019.
HG_T_4374_METAL_STRUCTURED_PACKINGS = [
    # --- Perforated Plate Corrugated (孔板波纹) — App. H ---
    PackingSpec(
        name="Metal structured Mellapak", material="SS", nominal_size_mm=125.0,
        specific_area_m2_m3=125.0, void_fraction=0.99, packing_factor_m_inv=33.0,
        shape_factor_onda=0.45, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        bain_hougen_A=0.291,
        source="HG/T 4374-2012 App. H + Kister Fp", notes="125Y; Fp from Kister GPDC",
    ),
    PackingSpec(
        name="Metal structured Mellapak", material="SS", nominal_size_mm=250.0,
        specific_area_m2_m3=250.0, void_fraction=0.975, packing_factor_m_inv=46.0,
        shape_factor_onda=0.45, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        bain_hougen_A=0.291,
        source="HG/T 4374-2012 App. H + Kister Fp", notes="250Y; Fp from Kister GPDC",
    ),
    PackingSpec(
        name="Metal structured Mellapak", material="SS", nominal_size_mm=350.0,
        specific_area_m2_m3=350.0, void_fraction=0.97, packing_factor_m_inv=56.0,
        shape_factor_onda=0.45, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        source="HG/T 4374-2012 App. H + Kister Fp", notes="350Y; Fp from Kister GPDC",
    ),
    PackingSpec(
        name="Metal structured Mellapak", material="SS", nominal_size_mm=500.0,
        specific_area_m2_m3=500.0, void_fraction=0.96, packing_factor_m_inv=89.0,
        shape_factor_onda=0.45, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        source="HG/T 4374-2012 App. H + Kister Fp", notes="500Y; Fp from Kister GPDC",
    ),

    # --- Wire Gauze (丝网波纹) — App. J ---
    PackingSpec(
        name="Metal wire gauze", material="SS", nominal_size_mm=250.0,
        specific_area_m2_m3=253.0, void_fraction=0.98, packing_factor_m_inv=20.0,
        shape_factor_onda=0.55, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        bain_hougen_A=0.30,
        source="HG/T 4374-2012 App. J", notes="250X; Fp is engineering estimate",
    ),
    PackingSpec(
        name="Metal wire gauze", material="SS", nominal_size_mm=500.0,
        specific_area_m2_m3=515.0, void_fraction=0.96, packing_factor_m_inv=30.0,
        shape_factor_onda=0.55, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        bain_hougen_A=0.30,
        source="HG/T 4374-2012 App. J", notes="500X; Fp is engineering estimate",
    ),
    PackingSpec(
        name="Metal wire gauze", material="SS", nominal_size_mm=700.0,
        specific_area_m2_m3=727.0, void_fraction=0.94, packing_factor_m_inv=43.0,
        shape_factor_onda=0.55, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        bain_hougen_A=0.30,
        source="HG/T 4374-2012 App. J", notes="700Y; Fp is engineering estimate",
    ),
]

GENERIC_PACKINGS = [
    PackingSpec(
        name="PP Pall ring", material="PP", nominal_size_mm=50.0,
        specific_area_m2_m3=102.0, void_fraction=0.92, packing_factor_m_inv=140.0,
        shape_factor_onda=1.45, critical_surface_tension_dyn_cm=31.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=0.698, billet_schultes_CFl=1.757, billet_schultes_CS=2.816, billet_schultes_Ch=0.593,
        bain_hougen_A=0.0942,
        source="Generic/vendor", notes="BS constants from Billet-Schultes 1999",
    ),
    PackingSpec(
        name="Metal Pall ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=112.0, void_fraction=0.95, packing_factor_m_inv=82.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=0.763, billet_schultes_CFl=1.580, billet_schultes_CS=2.725, billet_schultes_Ch=0.784,
        bain_hougen_A=0.10,
        source="Billet-Schultes 1999",
    ),
    PackingSpec(
        name="Ceramic Raschig ring", material="Ceramic", nominal_size_mm=25.0,
        specific_area_m2_m3=190.0, void_fraction=0.73, packing_factor_m_inv=587.0,
        shape_factor_onda=1.75, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08,
        billet_schultes_cp0=1.329, billet_schultes_CFl=1.899, billet_schultes_CS=2.454, billet_schultes_Ch=0.577,
        bain_hougen_A=0.022,
        source="Billet-Schultes 1999",
        mackowiak_group="saddle",
    ),
    PackingSpec(
        name="Ceramic Berl saddle", material="Ceramic", nominal_size_mm=25.0,
        specific_area_m2_m3=260.0, void_fraction=0.68, packing_factor_m_inv=787.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.35,
        bain_hougen_A=0.26,
        source="Billet-Schultes 1999",
        mackowiak_group="saddle",
    ),
]



# Additional packings from domestic packing research (diaoyan report)
# Parameters sourced from vendor data when HG/T standard not available
ADDITIONAL_PACKINGS = [
    # Ceramic Intalox Saddle (陶瓷矩鞍环)
    PackingSpec(
        name="Ceramic Intalox saddle", material="Ceramic", nominal_size_mm=25.0,
        specific_area_m2_m3=250.0, void_fraction=0.74, packing_factor_m_inv=617.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.10,
        bain_hougen_A=0.176,
        mackowiak_group="saddle",
        source="Vendor data (恒尔沃)", notes="Ceramic Intalox saddle parameters from vendor catalog",
    ),
    PackingSpec(
        name="Ceramic Intalox saddle", material="Ceramic", nominal_size_mm=38.0,
        specific_area_m2_m3=164.0, void_fraction=0.75, packing_factor_m_inv=389.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.05,
        bain_hougen_A=0.176,
        mackowiak_group="saddle",
        source="Vendor data (恒尔沃)", notes="Ceramic Intalox saddle parameters from vendor catalog",
    ),
    PackingSpec(
        name="Ceramic Intalox saddle", material="Ceramic", nominal_size_mm=50.0,
        specific_area_m2_m3=142.0, void_fraction=0.76, packing_factor_m_inv=323.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.00,
        bain_hougen_A=0.176,
        mackowiak_group="saddle",
        source="Vendor data (恒尔沃)", notes="Ceramic Intalox saddle parameters from vendor catalog",
    ),
    # Metal IMTP (金属环矩鞍)
    PackingSpec(
        name="Metal IMTP", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=185.0, void_fraction=0.96, packing_factor_m_inv=209.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.45,
        bain_hougen_A=0.06225,
        mackowiak_group="saddle",
        source="Vendor data", notes="Metal IMTP (Intalox Metal Tower Packing)",
    ),
    PackingSpec(
        name="Metal IMTP", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=75.0, void_fraction=0.96, packing_factor_m_inv=85.0,
        shape_factor_onda=1.40, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.38,
        bain_hougen_A=0.06225,
        mackowiak_group="saddle",
        source="Vendor data", notes="Metal IMTP (Intalox Metal Tower Packing)",
    ),
    # Ceramic Pall ring (陶瓷鲍尔环)
    PackingSpec(
        name="Ceramic Pall ring", material="Ceramic", nominal_size_mm=25.0,
        specific_area_m2_m3=210.0, void_fraction=0.73, packing_factor_m_inv=540.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.15,
        bain_hougen_A=0.10,
        source="Vendor data (恒尔沃)", notes="Ceramic Pall ring parameters from vendor catalog",
    ),
    PackingSpec(
        name="Ceramic Pall ring", material="Ceramic", nominal_size_mm=38.0,
        specific_area_m2_m3=140.0, void_fraction=0.75, packing_factor_m_inv=332.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.10,
        bain_hougen_A=0.10,
        source="Vendor data (恒尔沃)", notes="Ceramic Pall ring parameters from vendor catalog",
    ),
    PackingSpec(
        name="Ceramic Pall ring", material="Ceramic", nominal_size_mm=50.0,
        specific_area_m2_m3=100.0, void_fraction=0.78, packing_factor_m_inv=210.0,
        shape_factor_onda=1.60, critical_surface_tension_dyn_cm=61.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=1.05,
        bain_hougen_A=0.10,
        source="Vendor data (恒尔沃)", notes="Ceramic Pall ring parameters from vendor catalog",
    ),
    # Metal Cascade ring (金属阶梯环)
    PackingSpec(
        name="Metal Cascade ring", material="SS", nominal_size_mm=25.0,
        specific_area_m2_m3=221.0, void_fraction=0.951, packing_factor_m_inv=257.0,
        shape_factor_onda=1.35, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.42,
        bain_hougen_A=0.106,
        source="Vendor data", notes="Metal cascade mini ring (CMR)",
    ),
    PackingSpec(
        name="Metal Cascade ring", material="SS", nominal_size_mm=50.0,
        specific_area_m2_m3=109.0, void_fraction=0.961, packing_factor_m_inv=123.0,
        shape_factor_onda=1.35, critical_surface_tension_dyn_cm=75.0,
        min_wetting_rate_m3_m_h=0.08, billet_schultes_cp0=0.35,
        bain_hougen_A=0.106,
        source="Vendor data", notes="Metal cascade mini ring (CMR)",
    ),
]

def find_packing(name, size_mm, material=""):
    all_packings = (
        HG_T_3986_PLASTIC_PACKINGS
        + HG_T_4374_METAL_RANDOM_PACKINGS
        + HG_T_4374_METAL_STRUCTURED_PACKINGS
        + GENERIC_PACKINGS
        + ADDITIONAL_PACKINGS
    )
    for p in all_packings:
        if p.name == name and p.nominal_size_mm == size_mm:
            if not material or p.material == material:
                return p
    return None


def list_packings_by_name(name):
    all_packings = HG_T_3986_PLASTIC_PACKINGS + GENERIC_PACKINGS + ADDITIONAL_PACKINGS
    return [p for p in all_packings if p.name == name]


def get_billet_schultes_cp0(name, size_mm):
    p = find_packing(name, size_mm)
    return p.billet_schultes_cp0 if p else None


def get_bain_hougen_A(name, size_mm):
    p = find_packing(name, size_mm)
    return p.bain_hougen_A if p else None
