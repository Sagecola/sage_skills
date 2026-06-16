"""Ammonia tower design calculation engine.

Modules:
- _shared: constants, dataclasses, and utility functions
- pressure_drop_models: Blackwell, Billet-Schultes pressure drop correlations
- flooding_models: Blackwell, Kister GPDC, Bain-Hougen, Mackowiak SBD flooding
- flooding_models also includes Mackowiak SBD flooding; pressure_drop_models includes Mackowiak SBD pressure drop
- packing_data: packing parameter database (HG/T 3986, generic, vendor data)
- cli_parser: command-line argument parser
- report_formatter: text and Markdown report generators
- calculate_two_stage_ammonia_towers: main calculation entry point
"""

from ._shared import (
    SMALL,
    G,
    TowerHydraulics,
    diameter_from_flow,
    suggested_nominal_diameter_m,
)
from .pressure_drop_models import (
    BLACKWELL_DP_CONSTANTS,
    KISTER_GPDC_CONSTANTS,
    blackwell_abscissa,
    blackwell_pressure_drop_from_x,
    in_h2o_ft_to_pa_m,
    billet_schultes_pressure_drop,
    mackowiak_dry_pressure_drop,
    mackowiak_wet_pressure_drop,
    mackowiak_liquid_holdup,
)
from .flooding_models import (
    blackwell_flooding_ordinate,
    blackwell_velocity_from_ordinate,
    kister_gpdc_flooding_velocity,
    bain_hougen_flooding_velocity_si,
    mackowiak_flooding_velocity,
    eckert_chart_fit_hydraulics,
    convert_to_imperial,
)
