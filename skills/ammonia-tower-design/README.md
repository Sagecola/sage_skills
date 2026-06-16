# Ammonia Tower Design — 氨氮吹脱吸收填料塔设计

氨氮废水两段式吹脱+吸收填料塔的工程计算工具。适用于化工、环保行业的初步工艺设计。

## 功能

- **吹脱塔**：物料衡算 → 塔径 → 填料高度（Onda 传质）→ 润湿/循环校核
- **吸收塔**：水吸收（物理）+ 盐酸吸收（化学计量，气膜控制）
- **填料对比**：主方案 vs 对比方案并行计算

## 水力学模型

| 模型 | 用途 | 方法 |
|------|------|------|
| Blackwell-Kessler-Wankat | 操作点 + 泛点（默认） | GPDC 多项式拟合 |
| Kister GPDC | 泛点备选 | GPDC 分步法 |
| Mackowiak SBD | 泛点备选 | 液滴悬浮模型（精度最高 ~6%） |
| Billet-Schultes | 压降备选 | 几何驱动，适合国产填料 |
| Onda 关联 | 传质系数 | kGa, kLa, NTU/HTU |

## 填料数据

| 标准 | 材质 | 类型 | 条目 |
|------|------|------|------|
| HG/T 3986-2016 | PP 塑料 | 鲍尔环、阶梯环、花环(Taylor)、共轭环、海尔环、矩鞍环、扁环 | 31 条 |
| HG/T 4374-2012 | 不锈钢 | 拉西环、鲍尔环、阶梯环(CMR)、矩鞍环(IMTP)、共轭环、扁环、八四内弧环 + 规整填料 | 35 条 |

所有几何参数（a, ε）和干填料因子（φ）直接取自国标附录。

## 快速开始

```bash
cd skills/ammonia-tower-design

# 杭联示例（内置预设）
python -m scripts.calculate_two_stage_ammonia_towers --preset hanglian

# 预设 + 参数覆盖（切换泛点模型）
python -m scripts.calculate_two_stage_ammonia_towers \
  --preset hanglian --flooding-method mackowiak

# 自定义预设文件
python -m scripts.calculate_two_stage_ammonia_towers \
  --preset my-project.json --water-flow 0.8

# 生成设计计算书
python -m scripts.calculate_two_stage_ammonia_towers \
  --preset hanglian --write-markdown 设计计算书.md
```

预设文件格式见 `presets/hanglian.json`，复制一份修改参数即可复用。

## 文件结构

```
SKILL.md              AI 技能指令（给 AI 读）
README.md             本文件（给人读）
references/
  calculation-basis.md 公式、常数、模型文档
  document-style.md    设计文档写作规范
scripts/
  calculate_two_stage_ammonia_towers.py  主入口
  flooding_models.py                    泛点模型集合
  pressure_drop_models.py               压降模型集合
  packing_data.py                       填料参数数据库
  cli_parser.py                         CLI 参数解析
  report_formatter.py                   文本/Markdown 报告
```

## 默认策略

- 填料参数以 HG/T 国标为准，用户明确提供时以用户值为准
- 操作点按目标压降线（0.25 inH₂O/ft）确定，不按泛点率
- 形状因子 ψ、Cp0 等国标未提供的参数标注为工程估算
