"""Command-line argument parser and validator for ammonia tower design."""

from __future__ import annotations

import argparse

P_ATM_KPA = 101.325

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preliminary estimate for ammonia stripping plus water/HCl absorption towers."
    )
    parser.add_argument("--case", choices=["hanglian"], help="Load a built-in example case (shorthand for --preset).")
    parser.add_argument("--preset", type=str, default=None,
        help="Path to a JSON preset file, or name of a built-in preset (e.g. 'hanglian'). CLI arguments override preset values.")
    parser.add_argument("--water-flow", type=float, help="Wastewater flow in m3/h.")
    parser.add_argument("--influent-tan", type=float, help="Influent TAN in mg/L as N.")
    parser.add_argument("--effluent-tan", type=float, help="Effluent TAN in mg/L as N.")
    parser.add_argument("--removal-fraction", type=float, help="Target TAN removal fraction, e.g. 0.90.")
    parser.add_argument("--ph", type=float, help="Operating pH of the stripper.")
    parser.add_argument("--temperature", type=float, help="Operating temperature in degC.")
    parser.add_argument("--pressure", type=float, default=P_ATM_KPA, help="Operating pressure in kPa.")

    parser.add_argument(
        "--stripper-equilibrium-slope",
        type=float,
        default=0.752,
        help="Linear equilibrium slope m for y*=mx in the stripper.",
    )
    parser.add_argument(
        "--stripper-gas-inlet-y",
        type=float,
        default=0.0,
        help="Stripper inlet gas NH3 mole fraction.",
    )
    parser.add_argument(
        "--stripper-design-factor",
        type=float,
        default=2.0,
        help="Actual/minimum molar gas-liquid ratio factor for the stripper.",
    )
    parser.add_argument(
        "--stripper-pressure-drop-in-h2o-ft",
        type=float,
        default=0.25,
        help="Selected operating pressure drop for stripper hydraulics, inH2O/ft packing.",
    )
    parser.add_argument(
        "--stripper-flooding-pressure-drop-in-h2o-ft",
        type=float,
        default=2.5,
        help="Pressure-drop criterion used as a flooding proxy for stripper hydraulics, inH2O/ft.",
    )
    parser.add_argument(
        "--stripper-packing-area",
        type=float,
        default=127.0,
        help="Stripper packing specific area a_t in m2/m3.",
    )
    parser.add_argument(
        "--stripper-min-wetting-rate",
        type=float,
        default=0.08,
        help="Stripper minimum wetting rate Lw,min in m3/(m*h).",
    )
    parser.add_argument(
        "--stripper-height-safety-factor",
        type=float,
        default=1.2,
        help="Packing height safety factor for the stripper.",
    )
    parser.add_argument(
        "--stripper-main-packing-factor",
        type=float,
        default=180.0,
        help="Taylor-ring packing factor used in the transfer/flooding summary, 1/m.",
    )
    parser.add_argument(
        "--stripper-main-pressure-drop-packing-factor",
        type=float,
        default=180.0,
        help="Taylor-ring packing factor used in the explicit pressure-drop hydraulic fit, 1/m.",
    )
    parser.add_argument(
        "--stripper-main-shape-factor",
        type=float,
        default=1.50,
        help="Rosette ring (Taylor) Onda shape factor psi. Project default 1.50 is conservative; generic Rosette estimate is 1.55. HG/T 3986-2016 does not provide shape factors.",
    )
    parser.add_argument(
        "--stripper-main-critical-surface-tension-dyn-cm",
        type=float,
        default=31.0,
        help="Taylor-ring critical surface tension in dyn/cm. PP default is 31.",
    )
    parser.add_argument(
        "--stripper-main-flooding-density-correction",
        type=float,
        default=1.0,
        help="Liquid-density correction used in the Eckert flooding ordinate back-calculation.",
    )
    parser.add_argument(
        "--flooding-method",
        choices=["blackwell", "kister", "mackowiak"],
        default="blackwell",
        help="Flooding velocity correlation: 'blackwell' (Kessler-Wankat), 'kister' (Kister GPDC), or 'mackowiak' (Mackowiak SBD 2010).",
    )
    parser.add_argument(
        "--packing-type",
        choices=["random", "structured"],
        default="random",
        help="Packing type for Kister GPDC constants: 'random' or 'structured'.",
    )
    parser.add_argument(
        "--stripper-compare-packing-area",
        type=float,
        default=100.0,
        help="Comparison PP Pall-ring packing specific area a_t in m2/m3. HG/T 3986-2016 value.",
    )
    parser.add_argument(
        "--stripper-compare-min-wetting-rate",
        type=float,
        default=0.08,
        help="Comparison PP Pall-ring minimum wetting rate Lw,min in m3/(m*h).",
    )
    parser.add_argument(
        "--stripper-compare-packing-factor",
        type=float,
        default=128.0,
        help="Comparison PP Pall-ring flooding packing factor, 1/m. HG/T 3986-2016 App. A φ50 dry φ.",
    )
    parser.add_argument(
        "--stripper-compare-pressure-drop-packing-factor",
        type=float,
        default=128.0,
        help="Comparison PP Pall-ring pressure-drop packing factor, 1/m. Same as flooding factor for Pall rings.",
    )
    parser.add_argument(
        "--stripper-compare-shape-factor",
        type=float,
        default=1.45,
        help="Comparison PP Pall-ring Onda shape factor psi.",
    )
    parser.add_argument(
        "--stripper-compare-critical-surface-tension-dyn-cm",
        type=float,
        default=31.0,
        help="Comparison PP Pall-ring critical surface tension in dyn/cm. PP default is 31.",
    )
    parser.add_argument(
        "--stripper-compare-flooding-density-correction",
        type=float,
        default=1.0,
        help="Comparison PP Pall-ring density correction used in the Eckert scaling estimate.",
    )
    parser.add_argument(
        "--stripper-gas-density",
        type=float,
        default=1.18,
        help="Stripper gas density in kg/m3.",
    )
    parser.add_argument(
        "--stripper-gas-viscosity-pa-s",
        type=float,
        default=1.81e-5,
        help="Stripper gas viscosity in Pa*s.",
    )
    parser.add_argument(
        "--stripper-gas-diffusivity-m2-h",
        type=float,
        default=0.0713,
        help="Stripper NH3 gas-phase diffusivity in m2/h.",
    )
    parser.add_argument(
        "--stripper-liquid-density",
        type=float,
        default=998.2,
        help="Stripper liquid density in kg/m3.",
    )
    parser.add_argument(
        "--stripper-liquid-viscosity-pa-s",
        type=float,
        default=1.0e-3,
        help="Stripper liquid viscosity in Pa*s.",
    )
    parser.add_argument(
        "--stripper-liquid-diffusivity-m2-h",
        type=float,
        default=7.344e-6,
        help="Stripper NH3 liquid-phase diffusivity in m2/h.",
    )
    parser.add_argument(
        "--stripper-surface-tension-dyn-cm",
        type=float,
        default=72.75,
        help="Stripper liquid surface tension in dyn/cm.",
    )

    parser.add_argument(
        "--absorber-mode",
        choices=["water", "hcl", "both"],
        default="both",
        help="Absorber design basis: water absorption, HCl absorption, or both.",
    )
    parser.add_argument(
        "--absorber-capture-efficiency",
        type=float,
        default=0.99,
        help="NH3 capture efficiency in the absorber.",
    )
    parser.add_argument(
        "--absorber-outlet-ppmv",
        type=float,
        default=None,
        help="Target absorber outlet NH3 in ppmv. Overrides capture efficiency when provided.",
    )
    parser.add_argument(
        "--absorber-water-equilibrium-slope",
        type=float,
        default=0.754,
        help="Linear equilibrium slope m for water absorption, y*=mx.",
    )
    parser.add_argument(
        "--absorber-water-lg-factor",
        type=float,
        default=2.0,
        help="Actual/minimum molar liquid-gas ratio factor for the water absorber.",
    )
    parser.add_argument(
        "--absorber-water-inlet-x",
        type=float,
        default=0.0,
        help="Inlet liquid NH3 mole fraction for the water absorber.",
    )
    parser.add_argument(
        "--absorber-acid-weight-fraction",
        type=float,
        default=0.30,
        help="Hydrochloric acid mass fraction, e.g. 0.30 for 30 wt%%.",
    )
    parser.add_argument(
        "--absorber-acid-solution-density",
        type=float,
        default=1150.0,
        help="Hydrochloric acid solution density in kg/m3.",
    )
    parser.add_argument(
        "--absorber-acid-excess-factor",
        type=float,
        default=1.05,
        help="HCl stoichiometric excess factor.",
    )
    parser.add_argument(
        "--absorber-pressure-drop-in-h2o-ft",
        type=float,
        default=0.25,
        help="Selected operating pressure drop for absorber hydraulics, inH2O/ft packing.",
    )
    parser.add_argument(
        "--absorber-flooding-pressure-drop-in-h2o-ft",
        type=float,
        default=2.5,
        help="Pressure-drop criterion used as a flooding proxy for absorber hydraulics, inH2O/ft.",
    )
    parser.add_argument(
        "--absorber-packing-area",
        type=float,
        default=100.0,
        help="Absorber packing specific area a_t in m2/m3. HG/T 3986-2016 value for Pall ring DN50.",
    )
    parser.add_argument(
        "--absorber-packing-shape-factor",
        type=float,
        default=1.45,
        help="Absorber packing shape factor psi used in Onda correlations. Pall ring estimate.",
    )
    parser.add_argument(
        "--absorber-pressure-drop-packing-factor",
        type=float,
        default=128.0,
        help="Absorber packing factor for pressure-drop hydraulic fit, 1/m. HG/T 3986-2016 value.",
    )
    parser.add_argument(
        "--absorber-flooding-packing-factor",
        type=float,
        default=128.0,
        help="Absorber packing factor for flooding calculation, 1/m. HG/T 3986-2016 value.",
    )
    parser.add_argument(
        "--absorber-min-wetting-rate",
        type=float,
        default=0.08,
        help="Absorber minimum wetting rate Lw,min in m3/(m*h).",
    )
    parser.add_argument(
        "--absorber-total-liquid-flow",
        "--absorber-circulation-flow",
        dest="absorber_total_liquid_flow",
        type=float,
        default=None,
        help="Total liquid flow over the absorber packing in m3/h, including fresh liquid plus recycle.",
    )
    parser.add_argument(
        "--absorber-height-safety-factor",
        type=float,
        default=1.2,
        help="Packing height safety factor for the absorber.",
    )
    parser.add_argument(
        "--absorber-henry-inverse",
        type=float,
        default=0.725,
        help="Henry inverse H' for NH3-water in kmol/(m3*kPa), used for water absorption.",
    )
    parser.add_argument(
        "--absorber-gas-density",
        type=float,
        default=1.18,
        help="Absorber gas density in kg/m3.",
    )
    parser.add_argument(
        "--absorber-gas-viscosity-pa-s",
        type=float,
        default=1.81e-5,
        help="Absorber gas viscosity in Pa*s.",
    )
    parser.add_argument(
        "--absorber-gas-diffusivity-m2-h",
        type=float,
        default=0.0713,
        help="NH3 gas-phase diffusivity in m2/h.",
    )
    parser.add_argument(
        "--absorber-liquid-density",
        type=float,
        default=998.2,
        help="Absorber liquid density in kg/m3.",
    )
    parser.add_argument(
        "--absorber-liquid-viscosity-pa-s",
        type=float,
        default=1.0e-3,
        help="Absorber liquid viscosity in Pa*s.",
    )
    parser.add_argument(
        "--absorber-liquid-diffusivity-m2-h",
        type=float,
        default=7.344e-6,
        help="NH3 liquid-phase diffusivity in m2/h.",
    )
    parser.add_argument(
        "--absorber-surface-tension-dyn-cm",
        type=float,
        default=72.75,
        help="Absorber liquid surface tension in dyn/cm.",
    )
    parser.add_argument(
        "--absorber-critical-surface-tension-dyn-cm",
        type=float,
        default=54.0,
        help="Packing critical surface tension in dyn/cm.",
    )
    parser.add_argument(
        "--write-markdown",
        nargs="?",
        const="__AUTO__",
        default=None,
        help="Write a Markdown report to the specified path, or auto-generate a filename if no path given.",
    )
    parser.add_argument(
        "--markdown-title",
        type=str,
        default=None,
        help="Custom title for the Markdown report.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    return parser


def validate_args(args: argparse.Namespace) -> None:
    required = ["water_flow", "influent_tan", "ph", "temperature"]
    missing = [name for name in required if getattr(args, name) is None]
    if missing:
        raise ValueError(f"Missing required inputs: {', '.join(missing)}")
    if args.effluent_tan is None and args.removal_fraction is None:
        raise ValueError("Provide either --effluent-tan or --removal-fraction.")
    if args.water_flow <= 0.0:
        raise ValueError("Water flow must be positive.")
    if args.influent_tan <= 0.0:
        raise ValueError("Influent TAN must be positive.")
    if args.stripper_equilibrium_slope <= 0.0:
        raise ValueError("Stripper equilibrium slope must be positive.")
    if args.stripper_pressure_drop_in_h2o_ft <= 0.0:
        raise ValueError("Stripper pressure drop must be positive.")
    if args.stripper_flooding_pressure_drop_in_h2o_ft <= args.stripper_pressure_drop_in_h2o_ft:
        raise ValueError("Stripper flooding pressure drop must exceed operating pressure drop.")
    if args.absorber_capture_efficiency <= 0.0 or args.absorber_capture_efficiency >= 1.0:
        raise ValueError("Absorber capture efficiency must be between 0 and 1.")
    if args.absorber_pressure_drop_in_h2o_ft <= 0.0:
        raise ValueError("Absorber pressure drop must be positive.")
    if args.absorber_flooding_pressure_drop_in_h2o_ft <= args.absorber_pressure_drop_in_h2o_ft:
        raise ValueError("Absorber flooding pressure drop must exceed operating pressure drop.")
    if args.absorber_acid_weight_fraction <= 0.0 or args.absorber_acid_weight_fraction > 1.0:
        raise ValueError("Acid weight fraction must be within (0, 1].")
    if args.absorber_water_equilibrium_slope <= 0.0:
        raise ValueError("Water absorber equilibrium slope must be positive.")
    if args.absorber_water_lg_factor <= 0.0:
        raise ValueError("Water absorber L/G factor must be positive.")

