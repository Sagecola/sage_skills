# Ammonia Stripping And Absorption Tower Calculation Basis

## Scope

This reference captures the reusable calculation口径 for a two-stage ammonia-nitrogen wastewater treatment process:

1. A stripping packed tower transfers free ammonia from wastewater into air.
2. A downstream absorber transfers ammonia from the stripping gas into water or hydrochloric acid.

Use it for preliminary engineering design and calculation-note review. Treat final equipment selection as requiring vendor packing data and professional engineering review.

## Core Constants

Use these default molecular weights unless the project specifies otherwise:

| Symbol | Meaning | Value |
| --- | --- | --- |
| `M_N` | Nitrogen molecular weight | `14.007 kg/kmol` |
| `M_NH3` | Ammonia molecular weight | `17.031 kg/kmol` |
| `M_H2O` | Water molecular weight | `18.015 kg/kmol` |
| `M_HCl` | Hydrogen chloride molecular weight | `36.46 kg/kmol` |
| `P` | Default operating pressure | `101.325 kPa` |
| `R` | Gas constant | `8.314462618 kPa·m3/(kmol·K)` |

For water-like liquid at 25 degC, the local examples use:

| Symbol | Meaning | Typical value |
| --- | --- | --- |
| `rho_L` | Liquid density | `998.2 kg/m3` |
| `mu_L` | Liquid viscosity | `1.0e-3 Pa·s` |
| `sigma_L` | Surface tension | `72.75 dyn/cm` |
| `rho_G` | Air/gas density | `1.18 kg/m3` |
| `mu_G` | Gas viscosity | `1.81e-5 Pa·s` |
| `D_L` | NH3 liquid diffusivity | `7.344e-6 m2/h` |
| `D_G` | NH3 gas diffusivity | `0.0713 m2/h` |

## Ammonia As N Conversion

If the measured ammonia nitrogen is reported as `mg/L as N`, convert to free `NH3` equivalent before stripping calculations.

Free ammonia fraction:

```text
pKa = 0.09018 + 2729.92 / (T_C + 273.15)
f_NH3 = 1 / (1 + 10^(pKa - pH))
```

Ammonia equivalent:

```text
C_NH3 = C_N_as_N * f_NH3 * M_NH3 / M_N
```

For the Hanglian example at `pH = 12`, `T = 25 degC`, `C_N,in = 11000 mg/L as N`, the free ammonia fraction is about `0.99824`, giving `C_NH3,in = 13351.27 mg/L as NH3`.

## Stripping Tower Material Balance

Use a linear equilibrium relation unless better project equilibrium data are supplied:

```text
y* = m x
```

The local Hanglian example uses `m = 0.752` for ammonia stripping at 25 degC.

Approximate liquid mole fraction from concentration:

```text
n_NH3 = C_NH3_mg_L / 1000 / M_NH3
n_H2O = 1000 / M_H2O
x = n_NH3 / (n_NH3 + n_H2O)
```

Minimum molar gas/liquid ratio:

```text
(G'/L')_min = (x_in - x_out) / (m x_in - y_in)
```

Design gas/liquid ratio:

```text
G'/L' = beta * (G'/L')_min
```

The local example uses `beta = 2.0`.

Outlet gas ammonia mole fraction:

```text
y_out = y_in + (L'/G') * (x_in - x_out)
```

Gas volumetric flow:

```text
V_m = R (T_C + 273.15) / P
Q_G = G' * V_m
```

## Stripping Tower NTU And HTU

For stripping with linear equilibrium, define:

```text
S = L' / (m G')
```

Overall liquid-phase transfer unit number:

```text
N_OL = ln((1 - S) * (x_in - y_in/m) / (x_out - y_in/m) + S) / (1 - S)
```

Use the script-equivalent result where available rather than manually retyping complex formula variants.

Packing height:

```text
Z = N_OL * H_OL
Z_design = safety_factor * Z
```

The local examples use `safety_factor = 1.2`.

## Absorber Material Balance

### Water Absorption Basis

Use the design-example framework when the absorber is calculated as water absorption:

```text
y* = m x
y_out = y_in * (1 - eta_abs)
(L'/G')_min = (y_in - y_out) / (y_in/m - x_in)
L'/G' = beta_abs * (L'/G')_min
x_out = x_in + (y_in - y_out) / (L'/G')
```

The local examples use `m = 0.754`, `beta_abs = 2.0`, and often `eta_abs = 0.99` unless the user specifies a discharge target.

### HCl Absorption Basis

For hydrochloric acid absorption, use reaction stoichiometry for material balance:

```text
NH3 + HCl -> NH4Cl
n_NH3,captured = n_NH3,in * eta_abs
m_HCl,pure = n_NH3,captured * M_HCl * acid_excess_factor
m_acid_solution = m_HCl,pure / acid_weight_fraction
Q_acid,fresh = m_acid_solution / acid_solution_density
```

Default local values:

```text
acid_weight_fraction = 0.30
acid_excess_factor = 1.05
acid_solution_density = 1150 kg/m3
```

**Important: Gas-film controlled transfer**

The HCl absorption of NH3 is a classic case of gas-film controlled mass transfer:

1. **Extremely fast chemical reaction**: NH3 + H+ → NH4+ is an instantaneous irreversible ionic reaction. Once NH3 molecules diffuse through the gas film and enter the liquid phase, they are immediately consumed by the high concentration of H+.

2. **Negligible liquid-film resistance**: Due to the instantaneous reaction, the concentration gradient of NH3 in the liquid film is extremely steep. However, this is not caused by diffusion resistance but by the reaction result. The extremely fast reaction makes the liquid-film mass transfer resistance negligible.

3. **Main resistance in gas film**: The bottleneck of the entire process becomes the step where NH3 molecules diffuse from the gas phase through the gas film to the interface. As long as NH3 can pass through the gas film, the subsequent dissolution and reaction have almost no delay.

Therefore, the total mass transfer rate is completely determined by the diffusion rate of NH3 through the gas film. For packed-tower sizing, use the gas-film-controlled approximation:

```text
K_Ga ≈ k_Ga (gas-film coefficient)
H_OG = G_M' / (K_Ga * P * A)
N_OG = ln(y_in / y_out) (for instantaneous reaction)
Z = N_OG * H_OG
Z_design = safety_factor * Z
```

Because the fresh acid flow can be far below the minimum wetting requirement, distinguish:

```text
fresh liquid flow = stoichiometric acid solution feed
recycle liquid flow = extra circulation needed for hydraulic wetting
total liquid flow over packing = fresh + recycle
```

## Blackwell-Kessler-Wankat Correlation (Recommended)

Do not require the agent to read a chart image. Use the Blackwell-Kessler-Wankat explicit correlations from "Fortran Programs for Chemical Process Design" (Chapter 7, Mass Transfer). This is more accurate than simple power-law fits.

### Pressure Drop Correlation (Blackwell Model)

**Abscissa** (Equation 7-62):

```text
X = (L/G) * [rho_G / (rho_L - rho_G)]^0.5
```

**Ordinate** (Equation 7-63):

```text
Y = (G_1^2 * F_p * mu_L^0.1) / [rho_G * (rho_L - rho_G) * g]
```

where:
- G_1 = vapor mass velocity, lb/(ft²·s)
- F_p = packing factor, 1/ft
- mu_L = liquid viscosity, cP
- rho_L = liquid density, lb/ft³
- rho_G = vapor density, lb/ft³
- g = gravitational constant = 32.2 ft/s²

**Pressure Drop Correlation** (Equation 7-64):

```text
Y = exp[C_0 + C_1 * ln(X) + C_2 * (ln(X))² + C_3 * (ln(X))³ + C_4 * (ln(X))⁴]
```

**Constants for Each Pressure Drop** (Table 7-14):

| Pressure Drop (inH₂O/ft) | C₀ | C₁ | C₂ | C₃ | C₄ |
| --- | --- | --- | --- | --- | --- |
| 0.05 | -6.30253 | -0.60809 | -0.11932 | -0.00685 | 0.00032 |
| 0.10 | -5.50093 | -0.78508 | -0.13496 | 0.00134 | 0.00174 |
| 0.25 | -5.00319 | -0.95299 | -0.13930 | 0.01264 | 0.00334 |
| 0.50 | -4.39918 | -0.99404 | -0.16983 | 0.00873 | 0.00343 |
| 1.0 | -4.09505 | -1.00120 | -0.15871 | 0.00797 | 0.00318 |
| 1.5 | -4.02555 | -0.98945 | -0.08291 | 0.03237 | 0.00532 |

**Vapor Mass Velocity** (Equation 7-65):

```text
G_1 = { [Y * rho_G * (rho_L - rho_G) * g] / [F_p * mu_L^0.1] }^0.5
```

### Flooding Correlation (Kessler-Wankat Model)

**Flooding ordinate** (Equation 7-73):

```text
log(Y_f) = -1.6678 - 1.085 * log(X_f) - 0.29655 * (log(X_f))²
```

**Vapor rate at 70% flooding** (Equation 7-74):

```text
G_2 = 0.7 * [ (Y_f * rho_G * rho_L * g) / (F_p * Psi * mu_L^0.2) ]^0.5
```

**Vapor velocity at 70% flooding** (Equation 7-75):

```text
V_GF = G_2 / rho_G
```

where Psi = ratio of water density to liquid density (1.0 for water)

### Tower Sizing

**Tower cross-section** (Equation 7-66):

```text
A = G / (3600 * G_1)
```

**Tower diameter** (Equation 7-68):

```text
D = (4A / π)^0.5
```

### Unit Conversion Notes

- For SI units, convert:
  - L, G from kg/h to lb/h: multiply by 2.20462
  - rho from kg/m³ to lb/ft³: multiply by 0.06243
  - mu from Pa·s to cP: multiply by 1000
  - F_p from 1/m to 1/ft: multiply by 0.3048
  - g = 9.81 m/s² = 32.2 ft/s²

### Recommended Design Pressure Drop

| Service | Design Pressure Drop (inH₂O/ft) |
| --- | --- |
| Absorbers and Regenerators (Non-foaming) | 0.25–0.40 |
| Absorbers and Regenerators | 0.10–0.25 |
| Atmospheric or Pressure Stills and Fractionators | 0.40–0.80 |
| Vacuum Stills and Fractionators | 0.10–0.40 |

## Kister GPDC Correlation (Alternative)

Source: Wolf-Zöllner et al. 2019, "Extended performance comparison of different pressure drop, hold-up and flooding point correlations for packed columns", *Chemical Engineering Research and Design*. Constants from Kister et al. 2007, converted to numerical form by Tsai 2010 and extended to random packings by Wolf-Zöllner.

This is an alternative to the Blackwell-Kessler-Wankat correlation. The Kister GPDC is the original GPDC chart numerical implementation and showed the best agreement for pressure drop and flooding point in the Wolf-Zöllner 2019 evaluation (50 packings, two experimental databases).

### GPDC Pressure Drop (Equation 1)

**Capacity parameter**:

```text
CP = C1 * (ΔP/H)^C2 * [1 - exp(C6 * F_lv^C7)] / [1 + C3 * (ΔP/H)^(C2/C4) * F_lv^C5]^C4
```

**Flow parameter**:

```text
F_lv = (L/G) * (ρ_G / ρ_L)^0.5
```

where:
- `ΔP/H` = pressure drop per unit packing height, inH₂O/ft
- `L`, `G` = liquid and gas mass flow rates, lb/(ft²·s)
- `ρ_L`, `ρ_G` = liquid and gas densities, lb/ft³
- `C1–C7` = constants from table below

**Constants** (Table 5 of Wolf-Zöllner 2019):

| GPDC type | C₁ | C₂ | C₃ | C₄ | C₅ | C₆ | C₇ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Structured packings [in H₂O/ft] | 3.8617 | 0.6609 | 6.3763 | 0.7206 | 0.2898 | -0.9093 | -0.6819 |
| Random packings [in H₂O/ft] | 3.0 | 0.5778 | 5.3597 | 0.5545 | 0.4046 | -1.4234 | -0.6022 |

**Note**: The capacity parameter CP must be iterated to match the desired pressure drop ΔP/H, since CP depends on F_lv which in turn depends on the flow rates.

### Kister GPDC Flooding Point (Equations 2–6)

**Step 1 — Pressure drop at flooding** (Equation 2):

```text
ΔP_fl/H = 0.12 * Fp^0.7
```

where `Fp` = packing factor, 1/ft.

**Step 2 — Capacity parameter at flooding** (Equation 3, same form as Equation 1 with flooding constants):

```text
CP_fl = C1 * (ΔP_fl/H)^C2 * [1 - exp(C6 * F_lv^C7)] / [1 + C3 * (ΔP_fl/H)^(C2/C4) * F_lv^C5]^C4
```

Use the same C1–C7 constants from the table above. `F_lv` is the flow parameter at the operating condition.

**Step 3 — C-factor at flooding** (Equation 5):

```text
C_s,fl = CP_fl / (Fp^0.5 * ν^0.05)
```

where `ν` = kinematic viscosity of liquid, cSt (≈ 1.0 for water at 25 °C).

**Step 4 — Gas velocity at flooding** (Equation 6):

```text
u_s,fl = C_s,fl / √(ρ_G / (ρ_L - ρ_G))
```

### Kister GPDC vs Blackwell Comparison

| Aspect | Blackwell-Kessler-Wankat | Kister GPDC |
| --- | --- | --- |
| Pressure drop | Polynomial fit per pressure-drop line | Capacity parameter, unified equation |
| Flooding | Direct polynomial log(Y_f) vs log(X_f) | Stepwise: flooding ΔP → CP → C-factor → velocity |
| Constants | 6 sets of 5 constants (per ΔP line) | 7 constants (C₁–C₇, random/structured) |
| Source | Blackwell, Kessler, Wankat (book) | Kister, Tsai, Strigle (2007); Wolf-Zöllner 2019 |
| Validation | Local Hanglian example | 50 packings, MUL + SRP databases |

Both are valid GPDC-family methods. Wolf-Zöllner 2019 found Kister GPDC performed slightly better overall, but the difference is modest for random packings at atmospheric pressure.

## Tower Diameter Convention

Suggested nominal diameter convention from the local notes:

```text
if D < 1.0 m: round up to nearest 0.1 m
if D >= 1.0 m: round up to nearest 0.2 m
```

## Packing Defaults

Use vendor-confirmed packing data if available. If not, use these local preliminary values and mark uncertain values.

### Stripping Tower Main Option: PP Rosette Ring (Taylor) DN73

Per HG/T 3986-2016 Appendix D (花环). All values below are from the standard except shape factor and Cp0.

| Parameter | Value | Note |
| --- | --- | --- |
| `a_t` | `127 m2/m3` | HG/T 3986-2016 App. D |
| `phi_f` | `180 1/m` | HG/T 3986-2016 App. D dry packing factor |
| `phi_p` | `180 1/m` | Same as phi_f; wet packing factor may differ 10-20% |
| `L_w,min` | `0.08 m3/(m·h)` | DN73 < 75 mm, 散堆填料 convention |
| Onda shape factor `psi` | `1.50` | Engineering estimate (generic Rosette: 1.55). NOT from the standard. |
| Critical surface tension `sigma_c` | `31 dyn/cm` | PP default |

**Note**: HG/T 3986-2016 data is for PP (polypropylene) material. For other plastics, contact vendor for packing factor confirmation; geometric data (a, epsilon) remain valid.

### Comparison Option: PP Pall Ring DN50

Per HG/T 3986-2016 Appendix A (鲍尔环).

| Parameter | Value | Note |
| --- | --- | --- |
| `a_t` | `100 m2/m3` | HG/T 3986-2016 App. A |
| `phi_f` | `128 1/m` | HG/T 3986-2016 App. A dry packing factor |
| `phi_p` | `128 1/m` | Same as phi_f |
| `L_w,min` | `0.08 m3/(m·h)` | DN50 < 75 mm |
| Onda shape factor `psi` | `1.45` | Engineering estimate. NOT from the standard. |
| Critical surface tension `sigma_c` | `31 dyn/cm` for stripping, `54 dyn/cm` for absorber example basis |

### Published Packing Factors (from Blackwell-Kessler-Wankat / Eckert)

The following packing factors are from Table 7-13 of "Fortran Programs for Chemical Process Design" (Eckert). Use these when vendor data are unavailable.

**Pall Rings:**

| Material | Nominal Size (in) | Packing Factor Fp (1/ft) |
| --- | --- | --- |
| Plastic | 5/8 | 97 |
| Plastic | 1 | 52 |
| Plastic | 1 1/2 | 40 |
| Plastic | 2 | 25 |
| Plastic | 3 1/2 | 16 |
| Metal | 5/8 | 70 |
| Metal | 1 | 48 |
| Metal | 1 1/2 | 28 |
| Metal | 2 | 20 |
| Metal | 3 1/2 | 16 |

**Raschig Rings (Ceramic):**

| Nominal Size (in) | Packing Factor Fp (1/ft) |
| --- | --- |
| 3/8 | 1600 |
| 1/2 | 1000 |
| 5/8 | 580 |
| 3/4 | 380 |
| 1 | 255 |
| 1 1/4 | 155 |
| 1 1/2 | 125 |
| 2 | 95 |
| 3 | 65 |
| 3 1/2 | 37 |

**Raschig Rings (Metal, 1/32 in wall):**

| Nominal Size (in) | Packing Factor Fp (1/ft) |
| --- | --- |
| 5/8 | 700 |
| 1 | 390 |
| 1 1/2 | 300 |
| 2 | 170 |
| 3 | 155 |
| 3 1/2 | 115 |

**Berl Saddles (Ceramic):**

| Nominal Size (in) | Packing Factor Fp (1/ft) |
| --- | --- |
| 1/2 | 900 |
| 3/4 | 240 |
| 1 | 170 |
| 1 1/2 | 110 |
| 2 | 65 |
| 3 | 45 |

**Intalox Saddles (Ceramic):**

| Nominal Size (in) | Packing Factor Fp (1/ft) |
| --- | --- |
| 1/2 | 725 |
| 3/4 | 330 |
| 1 | 200 |
| 1 1/2 | 145 |
| 2 | 98 |
| 3 | 52 |
| 3 1/2 | 40 |

**Super Intalox (Plastic):**

| Nominal Size (in) | Packing Factor Fp (1/ft) |
| --- | --- |
| 1 | 33 |
| 2 | 21 |
| 3 | 16 |

**Note**: To convert packing factor from 1/ft to 1/m, multiply by 3.28084.

### Chinese Standard Random Packings (from HG/T 3986-2016)

Domestic plastic random packings per HG/T 3986-2016 "塑料塔填料". Geometric data (a, epsilon), bulk density, pieces per m³, and dry packing factor `φ` are taken directly from the standard appendices. The dry packing factor is directly usable in Blackwell/Kister GPDC models after unit conversion.

**Conversion**: `Fp (1/ft) = φ (1/m) / 3.28084`

**Plastic Pall Ring 鲍尔环 (App. A):**

| Diameter (mm) | Specific Area a (m²/m³) | Void Fraction ε (%) | Bulk Density (kg/m³) | Pieces/m³ | Dry φ (1/m) | Fp (1/ft) |
| --- | --- | --- | --- | --- | --- | --- |
| Φ16 | 274 | 90 | 91 | 177,000 | 376 | 115 |
| Φ25 | 213 | 91 | 85 | 48,000 | 283 | 86 |
| Φ38 | 151 | 91 | 82 | 16,000 | 200 | 61 |
| Φ50 | 100 | 92 | 76 | 6,300 | 128 | 39 |
| Φ76 | 72 | 92 | 73 | 1,800 | 92 | 28 |

**Plastic Cascade Ring 阶梯环 (App. B):**

| Diameter (mm) | Specific Area a (m²/m³) | Void Fraction ε (%) | Bulk Density (kg/m³) | Pieces/m³ | Dry φ (1/m) | Fp (1/ft) |
| --- | --- | --- | --- | --- | --- | --- |
| Φ16 | 346 | 85 | 134 | 297,000 | 563 | 172 |
| Φ25 | 214 | 91 | 81 | 81,000 | 284 | 87 |
| Φ38 | 172 | 93 | 62 | 27,000 | 214 | 65 |
| Φ50 | 121 | 93 | 62 | 10,700 | 150 | 46 |
| Φ76 | 84 | 93 | 63 | 3,400 | 104 | 32 |

**Plastic Rosette Ring 花环 (App. D):**

| Diameter (mm) | Specific Area a (m²/m³) | Void Fraction ε (%) | Bulk Density (kg/m³) | Pieces/m³ | Dry φ (1/m) | Fp (1/ft) |
| --- | --- | --- | --- | --- | --- | --- |
| Φ25 | 269 | 86 | 126 | 175,000 | 423 | 129 |
| Φ47 | 185 | 88 | 108 | 32,000 | 271 | 83 |
| Φ51 | 180 | 89 | 99 | 25,000 | 255 | 78 |
| Φ59 | 150 | 89 | 99 | 17,000 | 213 | 65 |
| Φ73 | 127 | 89 | 99 | 8,000 | 180 | 55 |
| Φ95 | 94 | 90 | 81 | 3,600 | 129 | 39 |
| Φ145 | 65 | 95 | 45 | 1,100 | 76 | 23 |

**Note**: These are dry packing factors from the standard. Wet packing factors may differ by 10-20%. For PP material, use critical surface tension σ_c = 31 dyn/cm. Onda shape factor ψ is not provided by the standard; use engineering estimates (Pall Ring ψ ≈ 1.45, Cascade Ring ψ ≈ 1.40, Rosette Ring ψ ≈ 1.55).

The standard also includes: 共轭环 (Conjugate ring, App. C), 海尔环 (Hiflow ring, App. E), 矩鞍环 (Intalox saddle, App. J), 扁环 (Flat ring, App. I). See `scripts/packing_data.py` for the complete database.

**Comparison with published foreign values**:

| Specification | HG/T 3986 φ (1/m) | Blackwell/Eckert Fp (1/ft) | Fp (1/m) equiv. | Deviation |
| --- | --- | --- | --- | --- |
| Pall Ring Φ50 | 128 | 40 (plastic 2 in) | 131 | -2% |
| Pall Ring Φ76 | 92 | 16 (plastic 3.5 in) | 52 | +77% |
| Pall Ring Φ38 | 200 | 40 (plastic 1.5 in) | 131 | +53% |
| Pall Ring Φ25 | 283 | 52 (plastic 1 in) | 171 | +66% |

The larger deviations for smaller sizes and Φ76 reflect differences in wall thickness and geometry between Chinese standard products and the US packings measured for the Eckert chart.

### Kister GPDC Packing Factors — Random Packings (from Wolf-Zöllner 2019, Table 6)

Packing factors for the Kister GPDC model (`Fp`) and Robbins model (`F_pd`). M = metal, P = plastic.

| Packing | Material | Robbins F_pd (1/ft) | Kister GPDC Fp (1/ft) |
| --- | --- | --- | --- |
| CMR 2 | M | 28° | 22* |
| CMR 2A | P | 27.7° | 30* |
| IMTP 40 | M | 27° | 24* |
| 1 in Pall Ring | M | 46° | 56* |
| 1 in Pall Ring | P | 50° | 27* |
| 2 in Pall Ring | M | 22° | 55* |
| RSR #0.3 | M | 57° | 57° |
| RSR #0.5 | M | 41° | 36° |
| RSR #0.7 | M | 14° | 16° |
| Hiflow 50-0 | P | 11° | 13* |
| Hiflow 50-6 | P | 7.5° | 11* |
| Raflux 25-5 | M | 52° | 56* |
| Raflux 50-5 | M | 26° | 27* |
| RMSR 25-3 | M | 35° | 41* |
| RMSR 50-4 | M | 16° | 18* |
| RMSR 70-5 | M | 7.5° | 12* |

° = this work (Wolf-Zöllner 2019), * = Kister 1992

### Kister GPDC Packing Factors — Structured Packings (from Wolf-Zöllner 2019, Table 7)

| Packing | Material | Robbins F_pd (1/ft) | Kister GPDC Fp (1/ft) |
| --- | --- | --- | --- |
| Mellagrid 64Y | M | 4.6° | 6* |
| Mellapak 125Y | M | 7.17° | 10* |
| Mellapak 200Y | M | 11.02° | 11* |
| Mellapak 200X | M | 5.5° | 5.5* |
| Mellapak 250X | M | 6.75° | 7* |
| Mellapak 250Y | M | 14.3° | 14* |
| Mellapak 250Y smooth | M | 12.2° | 14* |
| Mellapak 252Y | M | 10.56° | 12# |
| GTC 350Y | M | 17° | 23* |
| RMP S 350Y | M | 21.4° | 22* |
| Mellapak 500Y | M | 27.15° | 34* |
| RSP 200 | M | 9.5° | 12* |
| RSP 250 | M | 16.8° | 14* |
| RSP 300 | M | 15° | 17* |
| Hiflow Plus #1 | P | 10° | 12* |
| Hiflow Plus #2 | P | 5° | 8* |

° = this work (Wolf-Zöllner 2019), * = Kister 1992, # = extrapolated

**Note**: Grid structured packings (Mellagrid, Hiflow Plus, Raschig Super Pak) should use the structured packing constants (C₁–C₇) in the Kister GPDC equation, not the random packing constants. This was confirmed by Wolf-Zöllner 2019.

## Mackowiak SBD Correlation (Suspended Bed of Droplets)

The Mackowiak (2010) SBD model is a physically-based alternative to GPDC-family correlations. It models the packed bed as a suspended bed of droplets at flooding, requiring only geometric packing parameters (a, epsilon) rather than empirical packing factors. This makes it particularly valuable for 国产填料 where vendor packing factors may be uncertain or unavailable.

**Source**: Mackowiak, J. *Fluid Dynamics of Packed Columns*. Springer, 2010.

**Validation**: 1200+ flooding data points, 200 packing types, vacuum to 100 bar. Flooding prediction AARE ~6% — the best among published correlations per Wolf-Zöllner 2019 evaluation.

### Advantages for Chinese Packings

- **No packing factor required**: Uses `a` and `epsilon` directly from HG/T 3986-2016
- **Single packing parameter**: The dry resistance coefficient `psi` is estimated from geometry (Ergun-like `psi = 150/Re_V + 1.75`)
- **Insensitive to psi estimate**: Flooding velocity depends on `psi^(-1/6)` — a 50% error in psi gives only ~7% error in flooding velocity
- **Physical basis**: Droplet suspension mechanism rather than empirical chart fitting

### Flooding Velocity

```text
u_V,Fl = 0.80 * cos(alpha) * epsilon^(6/5) * psi^(-1/6) *
         [d_T * Delta_rho * g / rho_V]^(1/2) * [d_h/d_T]^(1/4) *
         (1 - h_L,Fl^0)^(7/2) * K_rhoV
```

Where:
- `alpha` = packing channel angle (0° for random packings, 30° X-type, 45° Y-type structured)
- `d_T = sqrt(sigma / (Delta_rho * g))` — droplet diameter (Laplace length)
- `d_h = 4 * epsilon / a` — hydraulic diameter
- `lambda_0 = (L/V) * (rho_V/rho_L)` — phase flow ratio
- `m = -0.82 + lambda_0/(lambda_0 + 0.5)` for turbulent (Re_L >= 2), or `m = -0.90 + ...` for laminar
- `h_L,Fl^0` — liquid holdup at flooding (calculated from lambda_0 and m)
- `K_rhoV = 1` for `rho_V <= 1.165 kg/m3`, or `(rho_V/1.165)^0.18` for higher densities

### Dry Pressure Drop

```text
dp = 6 * (1 - epsilon) / a
K = 1 + (2/3) * 1/(1-epsilon) * dp/D_c   (wall factor)
Re_V = u_V * dp / ((1-epsilon) * nu_V) * K
psi = 150/Re_V + 1.75
dP0/H = psi * (1-epsilon)/epsilon^3 * F_V^2 / (dp * K)
```

### Wet Pressure Drop (Below Loading Point)

```text
h_L = 0.055 * (u_L * epsilon / (g * dp))^(1/3) * (nu_L/nu_W)^0.1
Fr_L* = u_L^2 / (g * dp) * rho_L / Delta_rho
dP/H = dP0/H * (1 + C_B * Fr_L*^n) * (1 - h_L/epsilon)^(-3)
```

Where `n = 0.5` for laminar liquid (Re_L < 2), `n = 0.25` for turbulent.

### Packing Group Parameters

| Group | Packing types | C_B (laminar) | C_B (turbulent) |
|-------|-------------|---------------|-----------------|
| `raschig_pall` | Raschig rings, Pall rings, Cascade rings, Taylor/Rosette rings | 2.25 | 3.0 |
| `saddle` | Intalox saddles, IMTP, Berl saddles | 1.75 | 2.5 |
| `hiflow` | Hiflow rings, high-capacity packings | 1.4 | 2.0 |

### Comparison with GPDC Methods

| Aspect | Blackwell/Kister GPDC | Mackowiak SBD |
|--------|----------------------|---------------|
| Input parameters | Packing factor Fp | Geometric a, epsilon |
| Flooding prediction | Kessler-Wankat log-fit or Kister stepwise | Droplet suspension model |
| Accuracy (flooding) | ±15-30% | ±6% |
| Sensitivity to packing data | High (Fp directly affects result) | Low (psi^(-1/6) damping) |
| 国产填料适用性 | Limited by Fp availability | Good (uses a, epsilon from HG/T) |



## Billet-Schultes Correlation (For Chinese Standard Packings)

Use the Billet-Schultes (1999) correlation when working with国产填料 from HG/T 3986-2016 where packing factors are not available or unreliable. This model requires only geometric parameters (specific surface area `a` and void fraction `epsilon`) plus a packing-specific constant `Cp0`.

### Advantages for Chinese Packings

- **No packing factor required**: Uses `a` and `epsilon` directly from HG/T 3986-2016
- **Physical basis**: Derived from force balance, not purely empirical
- **Wide validation**: 3500+ data points, 50+ systems, 70+ packing types
- **Modern simulator standard**: Used in Aspen Plus, ProMax, etc.

### Key Equations

**Equivalent particle diameter:**
```text
dp = 6(1 - epsilon) / a
```

**Wall factor:**
```text
1/K = 1 + (2/3) * (1/(1-epsilon)) * (dp/Dc)
```

**Gas Reynolds number:**
```text
Re_G = u_G * dp / ((1-epsilon) * nu_G) * K
where nu_G = mu_G / rho_G
```

**Dry bed resistance coefficient:**
```text
psi_0 = Cp0 * (64/Re_G + 1.8/Re_G^0.08)
```

**Dry pressure drop:**
```text
dP/dz = psi_0 * (a/epsilon^3) * (F_G^2/2) * (1/K)
where F_G = u_G * sqrt(rho_G)
```

**Preloading liquid holdup:**
```text
h_L = [12 * mu_L * u_L * a / (g * rho_L)]^(1/3)
```

**Wet resistance coefficient:**
```text
psi_L = psi_0 * ((epsilon - h_L)/epsilon)^1.5
```

**Irrigated pressure drop:**
```text
dP/dz = psi_L * (a/(epsilon - h_L)^3) * (F_G^2/2) * (1/K)
```


### Cp0 Constants for Common Packings

| Packing | Material | Size (mm) | Cp0 | Source |
| --- | --- | --- | --- | --- |
| Pall ring | Metal | 50 | 0.40 | Billet-Schultes 1999 |
| Pall ring | PP | 25-76 | 0.40-0.55 | Estimate from metal Pall ring |
| Cascade ring (CMR) | PP | 25-50 | 0.38-0.45 | Geometric estimate |
| Rosette ring (花环) | PP | 25-73 | 0.45-0.60 | Engineering estimate |
| Taylor ring | PP | 73 | 0.52 | Project estimate |
| Raschig ring | Ceramic | 25 | 1.20 | Billet-Schultes 1999 |
| Berl saddle | Ceramic | 25 | 1.35 | Billet-Schultes 1999 |

**Note**: Cp0 values for 国产填料 (Cascade ring, Rosette ring, Taylor ring) are engineering estimates based on geometric similarity to validated packings. Vendor data or pilot testing should be used to confirm.

### HG/T 3986-2016 Verified Data vs Project Estimates

Geometric data (a, epsilon) and dry packing factor (φ) below are from HG/T 3986-2016 appendices. Shape factor, Cp0, and Bain-Hougen A are engineering estimates (NOT from the standard).

| Name | Size (mm) | a (m2/m3) | epsilon | Dry φ (1/m) | Shape ψ | Cp0 | Bain-Hougen A | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pall ring | 16 | 274 | 0.90 | 376 | 1.45 | 0.60 | 0.0942 | HG/T 3986 App. A |
| Pall ring | 25 | 213 | 0.91 | 283 | 1.45 | 0.55 | 0.0942 | HG/T 3986 App. A |
| Pall ring | 38 | 151 | 0.91 | 200 | 1.45 | 0.50 | 0.0942 | HG/T 3986 App. A |
| Pall ring | 50 | 100 | 0.92 | 128 | 1.45 | 0.45 | 0.0942 | HG/T 3986 App. A |
| Pall ring | 76 | 72 | 0.92 | 92 | 1.45 | 0.40 | 0.0942 | HG/T 3986 App. A |
| Cascade ring | 16 | 346 | 0.85 | 563 | 1.40 | 0.50 | 0.204 | HG/T 3986 App. B |
| Cascade ring | 25 | 214 | 0.91 | 284 | 1.40 | 0.45 | 0.204 | HG/T 3986 App. B |
| Cascade ring | 38 | 172 | 0.93 | 214 | 1.40 | 0.40 | 0.204 | HG/T 3986 App. B |
| Cascade ring | 50 | 121 | 0.93 | 150 | 1.40 | 0.38 | 0.204 | HG/T 3986 App. B |
| Cascade ring | 76 | 84 | 0.93 | 104 | 1.40 | 0.35 | 0.204 | HG/T 3986 App. B |
| Rosette ring | 25 | 269 | 0.86 | 423 | 1.55 | 0.60 | — | HG/T 3986 App. D |
| Rosette ring | 47 | 185 | 0.88 | 271 | 1.55 | 0.55 | — | HG/T 3986 App. D |
| Rosette ring | 51 | 180 | 0.89 | 255 | 1.55 | 0.50 | — | HG/T 3986 App. D |
| Rosette ring | 59 | 150 | 0.89 | 213 | 1.55 | 0.48 | — | HG/T 3986 App. D |
| Rosette ring (Taylor) | 73 | 127 | 0.89 | 180 | 1.55 | 0.50 | — | HG/T 3986 App. D |
| Rosette ring | 95 | 94 | 0.90 | 129 | 1.55 | 0.45 | — | HG/T 3986 App. D |
| Rosette ring | 145 | 65 | 0.95 | 76 | 1.55 | 0.40 | — | HG/T 3986 App. D |

Standard values are from HG/T 3986-2016 "塑料塔填料" (PP material only). Rosette ring (花环) is also marketed as Taylor ring (泰勒花环) — same product, different trade name. Shape factor ψ, Cp0, and Bain-Hougen A are NOT specified by the standard and remain engineering estimates. For other plastics (PE, PVC, PVDF etc.), geometric data (a, epsilon) remain valid but dry packing factor may differ; the standard says to scale bulk density by material density ratio.

Additional standard packings (共轭环 App. C, 海尔环 App. E, 矩鞍环 App. J, 扁环 App. I) are available in `scripts/packing_data.py`.

### Limitations

- Valid below the loading point. Above loading, liquid holdup increases with gas velocity and iterative solution is needed.
- Cp0 for国产填料 is estimated, not experimentally validated.
- Surface texture factor is set to 1.0 for smooth plastic; textured surfaces may need 1.1-1.3.
- At very low liquid rates, wet and dry pressure drops are nearly equal.

## Onda Correlation Notes

Use Onda correlations for effective wet area and film coefficients when reproducing this project.

**Liquid-film exponent**: The liquid-film exponent for the wetting expression is `2/3`. This is based on:

1. The original Onda correlation (1968) uses 2/3
2. The local design example numerical chain supports 2/3
3. The Python script `calculate_two_stage_ammonia_towers.py` uses 2/3

OCR text in some references may show 4/3 or 1/3, but these are likely OCR errors. If new experimental data suggests a different exponent, this should be updated.

Document enough intermediate values to make the result auditable:

- Effective wet area fraction `a_w/a_t`
- Wet packing area `a_w`
- Gas-film coefficient `k_Ga`
- Liquid-film coefficient `k_La`
- Overall coefficient `K_Ga`
- `N_OG` or `N_OL`
- `H_OG` or `H_OL`
- `Z` and `Z_design`

## Minimum Wetting And Circulation

Minimum spray density:

```text
W_min = L_w,min * a_t
```

Actual spray density:

```text
W = Q_L,total / A
```

Minimum total liquid flow over packing:

```text
Q_L,min = W_min * A
```

Required recycle/circulation:

```text
Q_recycle = max(Q_L,min - Q_fresh, 0)
Q_total = Q_fresh + Q_recycle
```

Do not confuse circulation flow with wastewater throughput or acid consumption. It is hydraulic liquid recirculated over the packing to keep the packing wetted.

## Hanglian Example Reference Results

For `Q_L = 0.5 m3/h`, `C_N,in = 11000 mg/L as N`, `removal = 90%`, `pH = 12`, `T = 25 degC`, main Taylor-ring stripper, Pall-ring absorber:

| Unit | Calculated diameter | Suggested nominal diameter | Design packing height |
| --- | --- | --- | --- |
| Stripper, PP Rosette ring (Taylor) DN73 | `0.584 m` | `DN600` | `2.915 m` |
| Stripper comparison, PP Pall ring DN50 | `0.533 m` | `DN600` | `3.528 m` |
| Water absorber | `0.500 m` | `DN500` | `4.174 m` |
| HCl absorber | `0.493 m` | `DN500` | `1.110 m` |

Circulation/wetting results:

| Unit | Required recycle/circulation |
| --- | --- |
| Stripper, Rosette ring (Taylor) | about `2.22 m3/h` |
| Stripper, Pall ring comparison | about `1.32 m3/h` |
| Water absorber | `0 m3/h` in the example |
| HCl absorber | about `2.326 m3/h` |

## Verification

After calculating, verify the results against:
1. The Python script `calculate_two_stage_ammonia_towers.py` output
2. The design example in `设计示例.md`
3. The reference results above

If results differ significantly, investigate the cause before proceeding. Common sources of discrepancy:
- Different packing factor values (phi_f vs phi_p)
- Different Onda correlation exponents (2/3 vs 4/3)
- Different safety factors (1.2 vs other values)
- Rounding errors in intermediate calculations


## Metal Packings — HG/T 4374-2012

HG/T 4374-2012 "金属塔填料技术条件" covers stainless steel and carbon steel random and structured packings. Material density = 7850 kg/m³. Carbon steel walls may be 20-50% thicker than the stainless steel values listed below; adjust specific area, void fraction, and packing factor accordingly.

### Metal Random Packings (散堆填料)

**Metal Pall Ring 鲍尔环 (App. C):**

| Size | a (m²/m³) | ε | Dry φ (1/m) | Pieces/m³ |
|------|-----------|-----|-------------|-----------|
| Φ16 | 362 | 0.95 | 423 | 214,000 |
| Φ25 | 219 | 0.95 | 255 | 51,940 |
| Φ38 | 146 | 0.96 | 165 | 15,180 |
| Φ50 | 109 | 0.96 | 124 | 6,500 |
| Φ76 | 71 | 0.96 | 80 | 1,830 |

**Metal Cascade Ring 阶梯环/CMR (App. D):**

| Size | a (m²/m³) | ε | Dry φ (1/m) | Pieces/m³ |
|------|-----------|-----|-------------|-----------|
| Φ25 | 221 | 0.95 | 257 | 98,120 |
| Φ38 | 153 | 0.96 | 173 | 30,040 |
| Φ50 | 109 | 0.96 | 123 | 12,340 |
| Φ76 | 75 | 0.96 | 85 | 3,540 |

**Metal IMTP 矩鞍环 (App. B):**

| Size | a (m²/m³) | ε | Dry φ (1/m) | Pieces/m³ |
|------|-----------|-----|-------------|-----------|
| Φ25 | 185 | 0.96 | 209 | 101,160 |
| Φ38 | 112 | 0.96 | 137 | 24,680 |
| Φ50 | 75 | 0.96 | 85 | 10,400 |
| Φ76 | 58 | 0.97 | 63 | 3,320 |

**Metal Raschig Ring 拉西环 (App. A):**

| Size | a (m²/m³) | ε | Dry φ (1/m) | Pieces/m³ |
|------|-----------|-----|-------------|-----------|
| Φ16 | 338 | 0.94 | 407 | 216,479 |
| Φ25 | 184 | 0.95 | 215 | 46,262 |
| Φ38 | 128 | 0.96 | 145 | 14,126 |
| Φ50 | 95 | 0.96 | 107 | 5,933 |
| Φ76 | 66 | 0.97 | 72 | 1,801 |

Other metal random packings in the standard: 共轭环 (App. E), 扁环/QH (App. F), 八四内弧环 (App. G). See `scripts/packing_data.py` for complete data.

### Metal Structured Packings (规整填料)

| Type | Model | a (m²/m³) | ε | Source |
|------|-------|-----------|-----|--------|
| 孔板波纹 | 125 | 125 | ~0.99 | App. H |
| 孔板波纹 | 250 | 250 | ~0.98 | App. H |
| 孔板波纹 | 350 | 350 | ~0.97 | App. H |
| 孔板波纹 | 500 | 500 | ~0.96 | App. H |
| 网孔板波纹 | 450X | 454 | 0.986 | App. I |
| 网孔板波纹 | 650Y | 651 | 0.976 | App. I |
| 丝网波纹 | 250X | 253 | ~0.98 | App. J |
| 丝网波纹 | 500X | 515 | ~0.96 | App. J |
| 丝网波纹 | 700Y | 727 | ~0.94 | App. J |

**Note**: HG/T 4374-2012 does not provide packing factors for structured packings. Use Kister GPDC factors from Wolf-Zöllner 2019 or vendor data. For the metal structured packings, use `--packing-type structured` with the Kister GPDC method.


## Additional References

### Comprehensive Packing Models Report

 contains a multi-agent research compilation covering:

- **8 flooding velocity models**: Bain-Hougen, Billet-Schultes (6-constant version), Mackowiak SBD, Kister-Gill/Piché, Eckert fits
- **7 pressure drop models**: Stichlmair, Billet-Schultes (full), Robbins, Mackowiak, Ergun
- **Chinese packing parameters**: Raschig ring, Tellerette/Rosette, Pall ring, CMR, Intalox/IMTP with vendor data
- **Programming examples**: Python implementations for all major models
- **Validation data**: Eckert flooding line coordinates, classic test cases

Use this report when:
- The user asks for model comparisons or alternative correlations
- Vendor data for国产填料 need cross-checking
- A third opinion on flooding/pressure drop is needed beyond Blackwell/Kister/Billet-Schultes
- Programming Bain-Hougen or Stichlmair models from scratch
