"""Text and Markdown report formatters for ammonia tower design."""

from __future__ import annotations

from dataclasses import asdict
import argparse
from typing import TYPE_CHECKING

try:
    from ._shared import suggested_nominal_diameter_m
except ImportError:
    from _shared import suggested_nominal_diameter_m  # type: ignore[no-redef]

if TYPE_CHECKING:
    try:
        from ._shared import TowerHydraulics
        from . import calculate_two_stage_ammonia_towers as _tower_mod
    except ImportError:
        from _shared import TowerHydraulics  # type: ignore[no-redef]
        import calculate_two_stage_ammonia_towers as _tower_mod  # type: ignore[no-redef]

def format_hydraulics(label: str, hydraulics: TowerHydraulics) -> list[str]:
    nominal_diameter = suggested_nominal_diameter_m(hydraulics.tower_diameter_m)
    lines = [
        label,
        f"  Gas flow: {hydraulics.gas_flow_m3_h:.1f} m3/h",
        f"  Liquid flow on packing: {hydraulics.liquid_flow_m3_h:.2f} m3/h",
        f"  Operating gas velocity: {hydraulics.operating_velocity_m_s:.2f} m/s",
        f"  Tower diameter: {hydraulics.tower_diameter_m:.2f} m",
        f"  Suggested nominal diameter: {nominal_diameter:.2f} m",
        f"  Pressure drop: {hydraulics.pressure_drop_pa_m:.1f} Pa/m" if hydraulics.pressure_drop_pa_m is not None else "  Pressure drop: n/a",
        f"  Spray density: {hydraulics.spray_density_m3_m2_h:.2f} m3/(m2*h)",
        f"  Minimum spray density: {hydraulics.min_spray_density_m3_m2_h:.2f} m3/(m2*h)",
        f"  Minimum liquid flow for wetting: {hydraulics.min_liquid_flow_m3_h:.2f} m3/h",
    ]
    if hydraulics.flooding_velocity_m_s is not None and hydraulics.flooding_fraction is not None:
        lines.insert(4, f"  Flooding gas velocity: {hydraulics.flooding_velocity_m_s:.2f} m/s")
        lines.insert(5, f"  Operating/flooding ratio: {hydraulics.flooding_fraction * 100:.1f}%")
    return lines


def format_stripper_packing(result: StripperPackingResults) -> list[str]:
    required_recycle_flow = max(result.hydraulics.min_liquid_flow_m3_h - result.hydraulics.liquid_flow_m3_h, 0.0)
    lines = [
        f"Stripper packing - {result.name} ({result.nominal_size}, {result.role})",
        f"  Packed tower size (D x Z_design): {result.hydraulics.tower_diameter_m:.2f} m x {result.design_packing_height_m:.2f} m",
        f"  Packing area a_t: {result.packing_specific_area_m2_m3:.1f} m2/m3",
        f"  Packing factor: {result.packing_factor_m_inv:.1f} 1/m",
        f"  Onda shape factor psi: {result.shape_factor:.2f}",
        f"  Critical surface tension: {result.critical_surface_tension_dyn_cm:.1f} dyn/cm",
        f"  Flooding basis: {result.flooding_basis}",
        f"  Blackwell abscissa X: {result.gpdc_abscissa:.4f}",
        f"  Blackwell operating ordinate Y: {result.operating_ordinate:.4f}",
        f"  Wet packing area a_w: {result.wet_packing_area_m2_m3:.2f} m2/m3",
        f"  Wet area fraction a_w/a: {result.wet_area_fraction:.3f}",
        f"  Corrected kGa: {result.gas_film_kga_kmol_m3_h_kpa:.3f} kmol/(m3*h*kPa)",
        f"  Corrected kLa: {result.liquid_film_kla_per_h:.3f} 1/h",
        f"  Overall KGa: {result.overall_kga_kmol_m3_h_kpa:.3f} kmol/(m3*h*kPa)",
        f"  Gas-phase HTU: {result.gas_phase_htu_m:.3f} m",
        f"  Liquid-phase HTU: {result.overall_liquid_htu_m:.3f} m",
        f"  Theoretical packing height: {result.theoretical_packing_height_m:.2f} m",
        f"  Design packing height: {result.design_packing_height_m:.2f} m",
        f"  Required recycle liquid for wetting: {required_recycle_flow:.2f} m3/h",
        "",
    ]
    if result.flooding_ordinate is not None:
        lines.insert(8, f"  Blackwell flood ordinate Y_f: {result.flooding_ordinate:.4f}")
    if result.flooding_density_correction is not None:
        lines.insert(9 if result.flooding_ordinate is not None else 8, f"  Density correction psi: {result.flooding_density_correction:.2f}")
    lines.extend(format_hydraulics(f"{result.name} hydraulics", result.hydraulics))
    if result.warnings:
        lines.extend(["", f"{result.name} warnings"])
        lines.extend(f"  - {warning}" for warning in result.warnings)
    return lines


def format_absorption(result: AbsorptionResults) -> list[str]:
    lines = [
        f"Absorber - {result.mode}",
        f"  Packed tower size (D x Z_design): {result.hydraulics.tower_diameter_m:.2f} m x {result.design_packing_height_m:.2f} m",
        f"  Inlet NH3: {result.inlet_nh3_mole_fraction * 1e6:.0f} ppmv",
        f"  Outlet NH3: {result.outlet_nh3_ppmv:.1f} ppmv",
        f"  Capture efficiency: {result.capture_efficiency * 100:.2f}%",
        f"  Captured NH3: {result.captured_nh3_kg_h:.3f} kg/h",
        f"  Fresh liquid flow: {result.fresh_liquid_flow_m3_h:.3f} m3/h",
        f"  Recycle liquid flow: {result.recycle_liquid_flow_m3_h:.3f} m3/h",
        f"  Total liquid flow on packing: {result.total_liquid_flow_m3_h:.3f} m3/h",
    ]
    if result.minimum_liquid_gas_ratio is not None and result.actual_liquid_gas_ratio is not None:
        lines.extend(
            [
                f"  Minimum L/G (molar): {result.minimum_liquid_gas_ratio:.4f}",
                f"  Actual L/G (molar): {result.actual_liquid_gas_ratio:.4f}",
            ]
        )
    if result.equilibrium_slope is not None:
        lines.append(f"  Equilibrium slope m: {result.equilibrium_slope:.4f}")
    if result.liquid_inlet_mole_fraction is not None and result.liquid_outlet_mole_fraction is not None:
        lines.append(f"  Liquid x_in -> x_out: {result.liquid_inlet_mole_fraction:.6f} -> {result.liquid_outlet_mole_fraction:.6f}")
    if result.pure_hcl_kg_h is not None:
        lines.extend(
            [
                f"  Pure HCl demand: {result.pure_hcl_kg_h:.3f} kg/h",
                f"  Fresh acid solution: {result.acid_solution_kg_h:.3f} kg/h",
                f"  Fresh acid solution volume: {result.acid_solution_m3_h:.3f} m3/h",
            ]
        )
    lines.extend(
        [
            f"  Wet area fraction a_w/a: {result.wet_area_fraction:.3f}",
            f"  Wet packing area a_w: {result.wet_packing_area_m2_m3:.2f} m2/m3",
            f"  Corrected kGa: {result.gas_film_kga_kmol_m3_h_kpa:.3f} kmol/(m3*h*kPa)",
            f"  Corrected kLa: {result.liquid_film_kla_per_h:.3f} 1/h",
            f"  Overall KGa: {result.overall_kga_kmol_m3_h_kpa:.3f} kmol/(m3*h*kPa)",
            f"  Gas-phase NTU: {result.gas_phase_ntu:.3f}",
            f"  Gas-phase HTU: {result.gas_phase_htu_m:.3f} m",
            f"  Theoretical packing height: {result.theoretical_packing_height_m:.2f} m",
            f"  Design packing height: {result.design_packing_height_m:.2f} m",
            "",
        ]
    )
    lines.extend(format_hydraulics(f"{result.mode} hydraulics", result.hydraulics))
    if result.warnings:
        lines.extend(["", f"{result.mode} warnings"])
        lines.extend(f"  - {warning}" for warning in result.warnings)
    return lines


def format_report(results: TwoStageResults) -> str:
    s = results.stripping
    lines = ["Two-stage ammonia tower estimate"]
    if results.case_name:
        lines.append(f"Case preset: {results.case_name}")

    lines.extend(
        [
            "",
            "Stripper basis",
            f"  Free NH3 fraction: {s.free_nh3_fraction * 100:.2f}%",
            f"  Influent NH3 equivalent: {s.influent_nh3_mg_l:.1f} mg/L as NH3",
            f"  Effluent NH3 equivalent: {s.effluent_nh3_mg_l:.1f} mg/L as NH3",
            f"  TAN removal: {s.removal_fraction * 100:.1f}%",
            f"  NH3-N removed: {s.removed_n_kg_h:.3f} kg/h as N",
            f"  NH3 removed: {s.removed_nh3_kg_h:.3f} kg/h as NH3",
            f"  Equilibrium slope m: {s.equilibrium_slope:.4f}",
            f"  Minimum G/L (molar): {s.minimum_molar_gas_liquid_ratio:.4f}",
            f"  Actual G/L (molar): {s.actual_molar_gas_liquid_ratio:.4f}",
            f"  Air/water ratio: {s.gas_liquid_volume_ratio:.1f} m3/m3",
            f"  Stripper outlet NH3: {s.outlet_gas_ppmv:.0f} ppmv",
            f"  Overall liquid NTU: {s.overall_liquid_ntu:.3f}",
            f"  Selected stripper packing: {s.selected_packing.name} {s.selected_packing.nominal_size}",
            f"  Selected liquid-phase HTU: {s.overall_liquid_htu_m:.3f} m",
            f"  Theoretical packing height: {s.theoretical_packing_height_m:.2f} m",
            f"  Design packing height: {s.design_packing_height_m:.2f} m",
            "",
        ]
    )
    lines.extend(format_stripper_packing(s.selected_packing))

    for packing in s.comparison_packings:
        lines.extend(["", *format_stripper_packing(packing)])

    if s.warnings:
        lines.extend(["", "Stripper warnings"])
        lines.extend(f"  - {warning}" for warning in s.warnings)

    for absorption in results.absorptions:
        lines.extend(["", *format_absorption(absorption)])

    return "\n".join(lines)


def markdown_title(args: argparse.Namespace, results: TwoStageResults) -> str:
    if args.markdown_title:
        return args.markdown_title
    if results.case_name == "hanglian":
        return "杭联示例两段塔设计计算"
    return "两段氨氮吹脱与吸收塔设计计算"


def format_formula_result(name: str, formula: str, value: str) -> list[str]:
    return [f"{name}：", "", "$$", formula, "$$", "", "$$", value, "$$", ""]


def format_markdown_report(args: argparse.Namespace, results: TwoStageResults) -> str:
    try:
        from .calculate_two_stage_ammonia_towers import resolve_effluent_tan
    except ImportError:
        from calculate_two_stage_ammonia_towers import resolve_effluent_tan  # type: ignore[no-redef]
    s = results.stripping
    selected = s.selected_packing
    comparison = s.comparison_packings[0] if s.comparison_packings else None
    lines: list[str] = [
        f"# {markdown_title(args, results)}",
        "",
        "对应脚本：",
        "",
        "```powershell",
        "python calculate_two_stage_ammonia_towers.py ...",
        "```",
        "",
        "## 1. 设计输入",
        "",
        "| 项目 | 取值 |",
        "| --- | --- |",
        f"| 废水流量 `Q_L` | `{args.water_flow:.4g} m3/h` |",
        f"| 进水氨氮 `C_{{N,in}}` | `{args.influent_tan:.6g} mg/L as N` |",
        f"| 出水氨氮 `C_{{N,out}}` | `{resolve_effluent_tan(args.influent_tan, args.effluent_tan, args.removal_fraction):.6g} mg/L as N` |",
        f"| 去除率 `η` | `{s.removal_fraction * 100:.2f}%` |",
        f"| pH | `{args.ph:.4g}` |",
        f"| 温度 `T` | `{args.temperature:.4g} °C` |",
        f"| 压力 `P` | `{args.pressure:.4f} kPa` |",
        "",
        "## 2. 吹脱塔",
        "",
        "### 2.1 物料衡算",
        "",
    ]

    lines.extend(
        format_formula_result(
            "游离氨分率 `f_{NH3}`",
            r"f_{NH_3} = \frac{1}{1 + 10^{(pK_a - pH)}}",
            rf"f_{{NH_3}} = {s.free_nh3_fraction:.6f} = {s.free_nh3_fraction * 100:.3f}\%",
        )
    )
    lines.extend(
        format_formula_result(
            "进水 `NH3` 当量",
            rf"C_{{NH_3,in}} = C_{{N,in}} \times f_{{NH_3}} \times \frac{{17.031}}{{14.007}}",
            rf"C_{{NH_3,in}} = {args.influent_tan:.6g} \times {s.free_nh3_fraction:.6f} \times \frac{{17.031}}{{14.007}} = {s.influent_nh3_mg_l:.2f}\ \mathrm{{mg/L}}",
        )
    )
    lines.extend(
        format_formula_result(
            "出水 `NH3` 当量",
            rf"C_{{NH_3,out}} = C_{{N,out}} \times f_{{NH_3}} \times \frac{{17.031}}{{14.007}}",
            rf"C_{{NH_3,out}} = {resolve_effluent_tan(args.influent_tan, args.effluent_tan, args.removal_fraction):.6g} \times {s.free_nh3_fraction:.6f} \times \frac{{17.031}}{{14.007}} = {s.effluent_nh3_mg_l:.2f}\ \mathrm{{mg/L}}",
        )
    )
    lines.extend(
        format_formula_result(
            "液相摩尔分数",
            r"x = \frac{n_{NH_3}}{n_{NH_3} + n_{H_2O}}",
            rf"x_2 = {s.influent_liquid_mole_fraction:.6f},\quad x_1 = {s.effluent_liquid_mole_fraction:.6f}",
        )
    )
    lines.extend(
        format_formula_result(
            "最小与实际摩尔气液比",
            r"\left(\frac{G'}{L'}\right)_{min} = \frac{x_2 - x_1}{mx_2 - y_1},\quad \frac{G'}{L'} = \beta \left(\frac{G'}{L'}\right)_{min}",
            rf"\left(\frac{{G'}}{{L'}}\right)_{{min}} = {s.minimum_molar_gas_liquid_ratio:.6f},\quad \frac{{G'}}{{L'}} = {s.actual_molar_gas_liquid_ratio:.6f}",
        )
    )
    lines.extend(
        format_formula_result(
            "空气量与尾气浓度",
            r"Q_G = G'V_m,\quad y_2 = y_1 + \frac{L'}{G'}(x_2 - x_1)",
            rf"Q_G = {s.air_flow_m3_h:.2f}\ \mathrm{{m^3/h}},\quad y_2 = {s.outlet_gas_mole_fraction:.8f} = {s.outlet_gas_ppmv:.1f}\ \mathrm{{ppmv}}",
        )
    )
    lines.extend(
        format_formula_result(
            "吹脱因子与液相总传质单元数",
            r"S = \frac{L'}{mG'},\quad N_{OL} = \frac{\ln\left[(1-S)\frac{x_2-y_1/m}{x_1-y_1/m} + S\right]}{1-S}",
            rf"S = {s.stripping_factor:.6f},\quad N_{{OL}} = {s.overall_liquid_ntu:.6f}",
        )
    )

    lines.extend(
        [
            "### 2.2 主方案水力学与传质",
            "",
            f"主方案填料：`{selected.name}`，公称尺寸：`{selected.nominal_size}`。",
            "",
        ]
    )
    lines.extend(
        format_formula_result(
            "Blackwell 横坐标",
            r"X = \frac{L_m}{G_m}\left(\frac{\rho_G}{\rho_L}\right)^{1/2}",
            rf"X = {selected.gpdc_abscissa:.6f}",
        )
    )
    if selected.flooding_ordinate is not None:
        lines.extend(
            format_formula_result(
                "操作点与泛点 (Blackwell GPDC)",
                r"Y_f = -1.6678 - 1.085\log X - 0.29655(\log X)^2,\quad Y_{op} = f(X, \Delta P)",
                rf"Y_f = {selected.flooding_ordinate:.6f},\quad Y_{{op}} = {selected.operating_ordinate:.6f}",
            )
        )
    else:
        lines.extend(
            format_formula_result(
                "泛点气速",
                r"u_f = f(\mathrm{Mackowiak\ SBD\ 2010})",
                rf"u_f = {selected.hydraulics.flooding_velocity_m_s:.4f}\ \mathrm{{m/s}}\ \text{{(Mackowiak SBD)}}",
            )
        )
    lines.extend(
        format_formula_result(
            "操作气速与塔径",
            r"u = \sqrt{\frac{Y_{op} g\rho_L}{\phi_p \psi_d \rho_G \mu_L^{0.2}}},\quad D=\sqrt{\frac{4A}{\pi}}",
            rf"u = {selected.hydraulics.operating_velocity_m_s:.4f}\ \mathrm{{m/s}},\quad D = {selected.hydraulics.tower_diameter_m:.4f}\ \mathrm{{m}}",
        )
    )
    lines.extend(
        format_formula_result(
            "润湿校核",
            r"W = \frac{Q_L}{A},\quad W_{min} = L_{w,min}a_t,\quad Q_{L,min}=W_{min}A",
            rf"W = {selected.hydraulics.spray_density_m3_m2_h:.4f}\ \mathrm{{m^3/(m^2\cdot h)}},\quad W_{{min}} = {selected.hydraulics.min_spray_density_m3_m2_h:.4f}\ \mathrm{{m^3/(m^2\cdot h)}},\quad Q_{{L,min}} = {selected.hydraulics.min_liquid_flow_m3_h:.4f}\ \mathrm{{m^3/h}}",
        )
    )
    lines.extend(
        format_formula_result(
            "Onda 关联结果",
            r"a_w = a_t\left(\frac{a_w}{a_t}\right),\quad K_Ga = \frac{1}{1/(k_Ga) + 1/(H'k_La)}",
            rf"\frac{{a_w}}{{a_t}} = {selected.wet_area_fraction:.6f},\quad a_w = {selected.wet_packing_area_m2_m3:.4f}\ \mathrm{{m^2/m^3}},\quad k_Ga = {selected.gas_film_kga_kmol_m3_h_kpa:.4f},\quad k_La = {selected.liquid_film_kla_per_h:.4f},\quad K_Ga = {selected.overall_kga_kmol_m3_h_kpa:.4f}",
        )
    )
    lines.extend(
        format_formula_result(
            "主方案填料高度",
            r"H_{OG}=\frac{G_M'}{K_GaPA},\quad H_{OL}=SH_{OG},\quad Z=N_{OL}H_{OL},\quad Z_{design}=1.2Z",
            rf"H_{{OG}} = {selected.gas_phase_htu_m:.6f}\ \mathrm{{m}},\quad H_{{OL}} = {selected.overall_liquid_htu_m:.6f}\ \mathrm{{m}},\quad Z = {selected.theoretical_packing_height_m:.6f}\ \mathrm{{m}},\quad Z_{{design}} = {selected.design_packing_height_m:.6f}\ \mathrm{{m}}",
        )
    )

    if comparison is not None:
        lines.extend(
            [
                "### 2.3 对比填料汇总",
                "",
                "| 项目 | 主方案 | 对比方案 |",
                "| --- | --- | --- |",
                f"| 填料 | `{selected.name}` | `{comparison.name}` |",
                f"| 塔径 | `{selected.hydraulics.tower_diameter_m:.3f} m` | `{comparison.hydraulics.tower_diameter_m:.3f} m` |",
                f"| 操作气速 | `{selected.hydraulics.operating_velocity_m_s:.3f} m/s` | `{comparison.hydraulics.operating_velocity_m_s:.3f} m/s` |",
                f"| 泛点气速 | `{selected.hydraulics.flooding_velocity_m_s:.3f} m/s` | `{comparison.hydraulics.flooding_velocity_m_s:.3f} m/s` |",
                f"| 泛点率 | `{selected.hydraulics.flooding_fraction * 100:.1f}%` | `{comparison.hydraulics.flooding_fraction * 100:.1f}%` |",
                f"| 最小润湿总液量 | `{selected.hydraulics.min_liquid_flow_m3_h:.3f} m3/h` | `{comparison.hydraulics.min_liquid_flow_m3_h:.3f} m3/h` |",
                f"| `H_OL` | `{selected.overall_liquid_htu_m:.3f} m` | `{comparison.overall_liquid_htu_m:.3f} m` |",
                f"| `Z_design` | `{selected.design_packing_height_m:.3f} m` | `{comparison.design_packing_height_m:.3f} m` |",
                "",
            ]
        )

    section_index = 3
    for absorption in results.absorptions:
        mode_title = "水吸收塔" if absorption.mode == "water" else "盐酸吸收塔"
        lines.extend([f"## {section_index}. {mode_title}", ""])
        if absorption.mode == "water":
            lines.extend(
                format_formula_result(
                    "设计目标",
                    r"y_{out} = y_{in}(1-\eta)",
                    rf"y_{{in}} = {absorption.inlet_nh3_mole_fraction:.8f},\quad y_{{out}} = {absorption.outlet_nh3_mole_fraction:.8f} = {absorption.outlet_nh3_ppmv:.2f}\ \mathrm{{ppmv}}",
                )
            )
            lines.extend(
                format_formula_result(
                    "最小与实际液气比",
                    r"\left(\frac{L'}{G'}\right)_{min} = \frac{y_{in}-y_{out}}{y_{in}/m-x_{in}},\quad \frac{L'}{G'} = \beta\left(\frac{L'}{G'}\right)_{min}",
                    rf"\left(\frac{{L'}}{{G'}}\right)_{{min}} = {absorption.minimum_liquid_gas_ratio:.6f},\quad \frac{{L'}}{{G'}} = {absorption.actual_liquid_gas_ratio:.6f}",
                )
            )
            lines.extend(
                format_formula_result(
                    "新鲜水量与出口液相浓度",
                    r"Q_{L,fresh} = \frac{L'M_{H_2O}}{\rho_L},\quad x_{out} = \frac{y_{in}-y_{out}}{L'/G'} + x_{in}",
                    rf"Q_{{L,fresh}} = {absorption.fresh_liquid_flow_m3_h:.6f}\ \mathrm{{m^3/h}},\quad x_{{out}} = {absorption.liquid_outlet_mole_fraction:.8f}",
                )
            )
        else:
            lines.extend(
                format_formula_result(
                    "酸耗量",
                    r"m_{HCl,pure}=n_{NH_3,cap}M_{HCl}\gamma,\quad m_{acid,sol}=\frac{m_{HCl,pure}}{w},\quad Q_{acid,fresh}=\frac{m_{acid,sol}}{\rho}",
                    rf"m_{{HCl,pure}} = {absorption.pure_hcl_kg_h:.6f}\ \mathrm{{kg/h}},\quad m_{{acid,sol}} = {absorption.acid_solution_kg_h:.6f}\ \mathrm{{kg/h}},\quad Q_{{acid,fresh}} = {absorption.acid_solution_m3_h:.6f}\ \mathrm{{m^3/h}}",
                )
            )

        lines.extend(
            format_formula_result(
                f"{mode_title}水力学",
                r"X = \frac{L_m}{G_m}\left(\frac{\rho_G}{\rho_L}\right)^{1/2},\quad D=\sqrt{\frac{4A}{\pi}},\quad W=\frac{Q_L}{A}",
                rf"D = {absorption.hydraulics.tower_diameter_m:.6f}\ \mathrm{{m}},\quad u = {absorption.hydraulics.operating_velocity_m_s:.6f}\ \mathrm{{m/s}},\quad u_f = {absorption.hydraulics.flooding_velocity_m_s:.6f}\ \mathrm{{m/s}},\quad W = {absorption.hydraulics.spray_density_m3_m2_h:.6f}\ \mathrm{{m^3/(m^2\cdot h)}},\quad Q_{{L,total}} = {absorption.total_liquid_flow_m3_h:.6f}\ \mathrm{{m^3/h}}",
            )
        )
        lines.extend(
            format_formula_result(
                f"{mode_title}传质与填料高度",
                r"H_{OG}=\frac{G_M'}{K_GaPA},\quad Z=N_{OG}H_{OG},\quad Z_{design}=1.2Z",
                rf"\frac{{a_w}}{{a_t}} = {absorption.wet_area_fraction:.6f},\quad a_w = {absorption.wet_packing_area_m2_m3:.6f},\quad k_Ga = {absorption.gas_film_kga_kmol_m3_h_kpa:.6f},\quad k_La = {absorption.liquid_film_kla_per_h:.6f},\quad K_Ga = {absorption.overall_kga_kmol_m3_h_kpa:.6f},\quad N_{{OG}} = {absorption.gas_phase_ntu:.6f},\quad H_{{OG}} = {absorption.gas_phase_htu_m:.6f}\ \mathrm{{m}},\quad Z_{{design}} = {absorption.design_packing_height_m:.6f}\ \mathrm{{m}}",
            )
        )
        section_index += 1

    lines.extend(
        [
            "## 5. 结果汇总",
            "",
            "| 单元 | 塔径 | 设计填料高度 | 备注 |",
            "| --- | --- | --- | --- |",
            f"| 吹脱塔主方案 | `{selected.hydraulics.tower_diameter_m:.3f} m` | `{selected.design_packing_height_m:.3f} m` | 最小润湿总液量 `{selected.hydraulics.min_liquid_flow_m3_h:.3f} m3/h` |",
        ]
    )
    if comparison is not None:
        lines.append(
            f"| 吹脱塔对比方案 | `{comparison.hydraulics.tower_diameter_m:.3f} m` | `{comparison.design_packing_height_m:.3f} m` | 最小润湿总液量 `{comparison.hydraulics.min_liquid_flow_m3_h:.3f} m3/h` |"
        )
    for absorption in results.absorptions:
        label = "水吸收塔" if absorption.mode == "water" else "盐酸吸收塔"
        remark = f"新鲜液量 `{absorption.fresh_liquid_flow_m3_h:.3f} m3/h`"
        if absorption.mode == "hcl":
            remark = f"纯 HCl `{absorption.pure_hcl_kg_h:.3f} kg/h`，新鲜酸液 `{absorption.fresh_liquid_flow_m3_h:.3f} m3/h`"
        lines.append(
            f"| {label} | `{absorption.hydraulics.tower_diameter_m:.3f} m` | `{absorption.design_packing_height_m:.3f} m` | {remark} |"
        )

    warnings: list[str] = []
    warnings.extend(s.warnings)
    warnings.extend(selected.warnings)
    if comparison is not None:
        warnings.extend(comparison.warnings)
    for absorption in results.absorptions:
        warnings.extend(absorption.warnings)
    unique_warnings = list(dict.fromkeys(warnings))
    if unique_warnings:
        lines.extend(["", "## 6. 说明与警告", ""])
        lines.extend(f"- {warning}" for warning in unique_warnings)

    return "\n".join(lines) + "\n"


