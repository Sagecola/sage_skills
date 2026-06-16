# Design Calculation Note Style

Use this reference when writing ammonia stripping/absorption tower calculation documents.

## Writing Philosophy

The script provides **numbers**. The AI provides **narrative and judgment**.
A good design note reads like an engineering report, not a code output:

- **Principles first** — briefly explain the mechanism before diving into numbers
- **Assumptions upfront** — state what's simplified and why
- **Step-by-step derivation** — "known condition → formula → substitution → result"
- **Judgment after each section** — does the result make sense? What needs attention?
- **The reader should be able to check every number by hand**

Reference example: `填料塔/氨氮吹脱工艺设计.md` in the project root.

## Preferred Structure

```markdown
# Project Name or Case Name

## 1. 设计基础 (Design Basis)

### 1.1 项目背景
1-2 sentences: source, scale, target.

### 1.2 设计参数
| Parameter | Value | Note |
| --- | --- | --- |
| Wastewater flow | ... m3/h | |
| Influent NH3-N | ... mg/L as N | |
| pH, temperature | ... | |
| Target removal | ... % | |
| Packing selected | ... | reason for choice |

### 1.3 基本假设
Numbered list of simplifying assumptions with brief justifications.

## 2. 吹脱塔计算 (Stripping Tower)

### 2.1 游离氨与物料衡算
Free NH3 fraction → NH3 equivalent concentration → mole fractions → 
minimum and actual G/L ratios → air flow → outlet gas concentration.

### 2.2 塔径确定
Packing data → Blackwell abscissa → operating/flooding ordinates → 
gas velocities → calculated diameter → nominal diameter (rounding per JB1153-73).

Include the rounding rationale explicitly.

### 2.3 填料高度
Stripping factor → N_OL → Onda coefficients (a_w/a, kGa, kLa, KGa) → 
H_OL → theoretical Z → design Z (×1.2 safety factor).

### 2.4 润湿与循环校核
Spray density vs minimum spray density. If below minimum, state required 
recirculation flow explicitly. Note whether the circulation is hydraulic-only 
or if it changes the mass balance.

### 2.5 对比填料（可选）
Same calculations for comparison packing. Summary comparison table.

## 3. 吸收塔计算 (Absorption Tower)

### 3.1 吸收方式
Water absorption or HCl absorption. State the basis and key assumptions.
For HCl: reaction stoichiometry, acid concentration, excess factor.
For water: linear equilibrium, minimum L/G.

### 3.2 塔径确定
Same structure as stripper.

### 3.3 填料高度
N_OG or N_OL → Onda coefficients → H_OG → theoretical Z → design Z.

### 3.4 润湿与循环校核
Fresh liquid vs minimum wetting → circulation required. Distinguish clearly
between fresh liquid flow and total flow over packing.

## 4. 压降（可选）
Blackwell operating pressure drop (design basis). Alternative models if 
comparison is requested.

## 5. 结果汇总 (Results Summary)

| Unit | Packing | D_calc | DN | Z_theo | Z_design | Circulation | Flood% | ΔP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Stripper | ... | ... | ... | ... | ... | ... | ... | ... |
| Absorber | ... | ... | ... | ... | ... | ... | ... | ... |

## 6. 讨论与建议 (Discussion)
Not all sections are always needed; include those relevant to the case.

### 6.1 塔径合理性
- Diameter/packing-size ratio (should be > 10-15 for random packings)
- Flooding percentage (50-85% acceptable for non-foaming; <50% for foaming)
- Wall effect if D < 300mm

### 6.2 润湿与布液
- Is spray density adequate without circulation?
- If circulation is needed, what pump capacity?
- Liquid distributor type recommendation based on diameter

### 6.3 工程不确定性
- Which parameters are estimates vs vendor-confirmed?
- Sensitivity: what changes if packing factor is ±20%?
- Recommendations for further verification (pilot test, vendor data)

## 7. 假设与说明 (Assumptions and Notes)
Bulleted list of all assumptions and data sources used.
```

## Writing Rules

### Formula Presentation

Every calculation step follows this pattern:

1. **Known condition** — state what's given
2. **Formula** — LaTeX, define all symbols
3. **Substitution** — plug in actual values
4. **Numeric result** — with units
5. **Engineering interpretation** — if result warrants comment

Example:

```markdown
已知废水水量 L_M = 0.5 m³/h，进水摩尔流速为：

$$
L_M' = \frac{L_M \times 1000}{M_{H_2O}} = \frac{0.5 \times 1000}{18.015} = 27.76\ \mathrm{kmol/h}
$$

式中：M_{H_2O} 为水的摩尔质量，18.015 g/mol。
```

### Naming Conventions

- Design packing height: `设计填料层高度` or `design packing height Z_design`
- Never call it "tower height" unless vessel internals are also calculated
- Calculated diameter vs nominal diameter: always show both
- "Circulation" = hydraulic liquid recycled over packing for wetting, NOT wastewater throughput

### Engineering Judgments Required

After each major section, include at least one of:
- Comparison to rule-of-thumb range
- Flag if result is unusual
- Note if the result depends on an uncertain input
- Recommendation for next step

### Assumption Labeling

Label uncertain values at the point of use, not buried in a final disclaimer:

- "Onda shape factor ψ = 1.50 (engineering estimate; HG/T 3986 does not specify ψ)"
- "Packing factor φ = 180 1/m (HG/T 3986-2016 App. D 花环 Φ73 dry packing factor)"
- "HCl absorber sizing: gas-film-controlled approximation (NH₃ + H⁺ reaction is instantaneous)"

### Table Formats

| Item | Value | Source/Note |
| --- | --- | --- |
| ... | ... | ... |

Always include a source or note column in parameter tables.

## Result Summary Table

Include near the top (for quick reference) and at the end (for final record):

```markdown
| Unit | Packing | D_calc | DN | Z_design | Circulation | ΔP | Flood% |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Stripper | Rosette ring (Taylor) DN73 | 0.xxx m | DNxxx | x.xxx m | x.xx m3/h | xxx Pa/m | xx% |
| Absorber | Pall ring DN50 | 0.xxx m | DNxxx | x.xxx m | x.xx m3/h | xxx Pa/m | xx% |
```

## Quality Checklist

Before finalizing the document, verify:
- [ ] Every symbol in every formula is defined
- [ ] All ammonia concentrations clearly labeled as N or NH₃
- [ ] Diameter rounding rationale stated
- [ ] D/d ratio checked (>10-15 for random packings)
- [ ] Flooding % in acceptable range (or flagged if not)
- [ ] Wetting check passed (or circulation flow specified)
- [ ] Uncertain parameters labeled at point of use
- [ ] Results cross-checked against script output
