---
name: ammonia-tower-design
description: Ammonia nitrogen stripping and absorption packed-tower design workflow for wastewater treatment. Use when Codex needs to calculate, review, or document a two-stage process that strips ammonia from water into air and then absorbs ammonia from off-gas into water or hydrochloric acid; includes tower diameter, design packing height, packing comparison, wetting/circulation checks, Eckert/GPDC explicit-fit hydraulics, and Onda mass-transfer sizing.
---

# Ammonia Tower Design

## Workflow

Use this skill for ammonia-nitrogen packed tower calculations and calculation-note drafting.

1. Confirm whether influent ammonia is reported as `mg/L as N`. If yes, convert to `NH3` using `M_NH3 / M_N`, and apply free-ammonia fraction from pH and temperature.
2. Separate the process into two units: the stripping tower transfers `NH3` from liquid to air; the downstream absorber transfers `NH3` from gas into water or HCl solution.
3. Read `references/calculation-basis.md` before doing numerical calculations or reviewing formulas.
4. Read `references/document-style.md` before writing a design note or calculation report.
5. Use the Python calculator in `scripts/calculate_two_stage_ammonia_towers.py` for arithmetic. Do not edit the script unless the user asks. If a new calculator is needed, create a new script and keep it calculation-only.

## Required Outputs

Always make the key equipment sizes explicit:

- Stripping tower calculated diameter `D`, suggested nominal diameter, theoretical packing height, and design packing height `Z_design`.
- Absorption tower calculated diameter `D`, suggested nominal diameter, theoretical packing height, and design packing height `Z_design`.
- Fresh liquid flow, recycle/circulation flow, and total liquid flow over the packing for absorbers.
- Minimum wetting check for each tower.
- Warnings where values are engineering estimates rather than vendor-confirmed data.

Use "tower height" carefully. Unless vessel internals and mechanical clearances are specified, call the result **design packing height**, not whole tower height.

## Calculation Policy

Use explicit formulas rather than manual chart reading when possible. The Python calculator uses the Blackwell-Kessler-Wankat correlation for hydraulic calculations by default.

Alternative methods (select via `--flooding-method`):
- **Kister GPDC** (`kister`, Kister et al. 2007, validated by Wolf-Zöllner et al. 2019): Use when vendor packing factors use the Kister Fp convention or when a second opinion is needed.
- **Mackowiak SBD** (`mackowiak`, Mackowiak 2010): Suspended bed of droplets model. **Best flooding prediction accuracy** (~6% AARE based on 1200+ data points, 200 packing types). Requires only geometric parameters (a, epsilon). Particularly useful for 国产填料 where packing factors are uncertain — the model estimates dry resistance coefficient from geometry rather than relying on vendor-supplied packing factors.
- **Billet-Schultes** (Billet & Schultes 1999): Use for 国产填料 from HG/T 3986-2016 where packing factors are unavailable. This model requires only geometric parameters (a, epsilon) and a packing-specific Cp0 constant. The calculator includes a packing parameter database in `scripts/packing_data.py` with HG/T 3986-2016 data.

**Important**: The flooding method only affects flooding velocity prediction. The operating point (tower diameter) is always determined from the Blackwell pressure-drop correlation at the specified operating pressure drop (default 0.25 inH₂O/ft). This is because the operating point is sized for a target pressure drop, not for a target fraction of flooding.

For packing selection, use PP Rosette ring (Taylor ring / 泰勒花环) DN73 as the main stripping-tower option and compare against PP Pall ring DN50. All PP packing geometric data and dry packing factors should reference HG/T 3986-2016 (the Chinese national standard for plastic tower packings). The standard covers PP material only; for other plastics (PE, PVC, etc.), geometric data remain valid but bulk density must be scaled by material density ratio.

Rosette ring Φ73 per HG/T 3986-2016 App. D: a=127 m²/m³, ε=0.89, φ=180 1/m. Shape factor (ψ) and Cp0 are NOT specified by the standard and remain engineering estimates.

Published packing factors and Billet-Schultes Cp0 constants for common packings and Chinese standard packings are available in `references/calculation-basis.md` and `scripts/packing_data.py`:

- **HG/T 3986-2016** (塑料塔填料): PP Pall Ring, Cascade Ring, Rosette Ring (Taylor), Conjugate Ring, Hiflow Ring, Intalox Saddle, Flat Ring
- **HG/T 4374-2012** (金属塔填料): Metal Pall Ring, Cascade Ring (CMR), IMTP, Raschig Ring, Conjugate Ring, Flat Ring (QH), 八四内弧环, plus structured packings (孔板波纹, 丝网波纹)

Both standards provide geometric data (a, epsilon) and dry packing factor (φ) suitable for Blackwell/Kister GPDC models.

For HCl absorption, use reaction stoichiometry for material balance and a gas-film-controlled packed-tower sizing approximation. This is valid because:

1. The chemical reaction NH3 + H+ → NH4+ is instantaneous and irreversible
2. The liquid-film resistance is negligible due to the extremely fast reaction
3. The main mass transfer resistance is in the gas film

Also offer a water-absorption basis if the user asks for a conservative/design-example-style comparison.

## Documentation Rule

**Do not use `--write-markdown` for the final design note** unless the user specifically requests a quick dump. The script-generated report is a mechanical data listing — it lacks engineering narrative.

Instead, follow this workflow for producing a design calculation note:

1. Run the calculator (`python -m scripts.calculate_two_stage_ammonia_towers --case hanglian ...`) to get all numeric results.
2. Read `references/document-style.md` for the full document template and writing rules.
3. Write the design note manually, section by section, using the **"known condition → formula → substitution → result → interpretation"** pattern. Reference the project's `填料塔/氨氮吹脱工艺设计.md` as a style example.
4. After each major section, add engineering judgment: Does the diameter make sense? Is flooding % in range? Is wetting adequate? What depends on uncertain inputs?
5. Include a Discussion section covering at minimum: diameter adequacy (D/d ratio, wall effects), flooding margin, wetting/circulation needs, and a candid list of which numbers are estimates vs vendor-confirmed.

The script provides numbers. You provide judgment. The reader should be able to verify every calculation step by hand.

When results depend on uncertain assumptions, state the assumption next to the number, not only in a final disclaimer.

## Verification

After calculating, verify the results against:
1. The Hanglian example reference results in `calculation-basis.md`
2. The Python script `calculate_two_stage_ammonia_towers.py` output
3. The design example in `设计示例.md`

If results differ significantly, investigate the cause before proceeding.

## Assumption Labeling

Label uncertain engineering assumptions at the point of use:

- Taylor-ring Onda shape factor `psi = 1.50`: engineering estimate. (Standard 花环 ψ ≈ 1.55.)
- Taylor-ring packing factor `phi = 180 1/m`: matches HG/T 3986-2016 App. D 花环 Φ73 dry packing factor. Geometric data (a=127, epsilon≈0.90) also consistent with the standard.
- HCl absorber transfer sizing: gas-film-controlled approximation (valid because NH3 + H+ reaction is instantaneous).
