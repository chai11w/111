# ROI 异常预警分析 MVP

本项目是跨境电商广告数据 AI 监控与预警工具的第一版 MVP。

当前只实现一个最小模块：ROI 异常预警分析模块。

## MVP 边界

- 输入：模拟 CSV 广告数据，位置为 `data/ad_data_sample.csv`。
- 初筛：由确定性 ROI 阈值判断异常广告。
- LLM：不判断 ROI 是否达标，只分析已经被阈值筛出的异常广告。
- 输出：Markdown 预警报告，生成到 `reports/roi_alert_report.md`。
- 第一版不自动调整预算，只输出预警和建议。
- 当前 LLM 为离线模拟分析层，不调用真实 LLM API。

## 当前目录

```text
data/
  ad_data_sample.csv
src/
reports/
skills/
  roi-anomaly-analysis/
```

## 模拟数据字段

`data/ad_data_sample.csv` 包含以下字段：

```text
date,platform,owner,category,campaign_name,ad_name,spend,revenue,orders,clicks,impressions,ctr,cpa,roi
```

样本覆盖 Facebook、Google、TikTok 三个平台，并包含低效广告、正常广告、优质广告三类数据。

`owner` 表示投手，`category` 表示投手负责的品类。当前模拟了 3 个投手：

```text
Alice -> Beauty
Ben -> Electronics
Cindy -> Home
```

## 当前能力

当前已实现 ROI 阈值初筛逻辑：

- ROI 低于低效阈值，标记为低效广告。
- ROI 高于优质阈值，标记为优质广告。
- ROI 正常，暂时不进入 LLM 分析。

默认阈值：

```text
低效广告：roi < 1.2
优质广告：roi > 3.0
```

初筛后的异常广告会整理为 `AlertCase` 结构化对象，包含：

- `alert_type`：异常类型，当前为 `低效广告` 或 `优质广告`。
- `trigger_rule`：触发规则，例如 `roi < 1.2`。
- `metrics`：关键指标，包括 `spend`、`revenue`、`orders`、`clicks`、`impressions`、`ctr`、`cpa`、`roi`。

项目内分析流程已沉淀到 `skills/roi-anomaly-analysis/SKILL.md`。后续 LLM 分析层或离线占位分析器应按该流程分析 `AlertCase`，只做原因分析和建议生成，不重新判断 ROI 是否异常。

当前已实现离线 LLM 分析层：`src/llm_analyzer.py`。它会读取 ROI 初筛结果，按项目内分析流程生成可能原因、建议动作和人工确认项，并输出 Markdown 预警报告。

## 如何运行

从项目根目录执行以下命令。

1. 运行 ROI 初筛：

```powershell
python src/roi_filter.py --input data/ad_data_sample.csv
```

2. 生成 Markdown 预警报告：

```powershell
python src/llm_analyzer.py --input data/ad_data_sample.csv --output reports/roi_alert_report.md
```

3. 运行测试：

```powershell
python -m unittest discover -s tests
```

## 输入与输出

输入文件：

```text
data/ad_data_sample.csv
```

输入含义：

- 用模拟 CSV 表示从统一广告后台提取到的广告数据。
- 当前字段包括平台、投手、品类、广告系列、广告名、花费、收入、订单数、点击数、展示数、点击率、转化成本和 ROI。
- 当前样本覆盖 Facebook、Google、TikTok 三个平台。

输出文件：

```text
reports/roi_alert_report.md
```

输出内容：

- 异常广告清单
- 触发规则
- 关键数据
- 优先级
- 可能原因
- 建议动作
- 需人工确认的信息

## LLM 状态说明

当前版本中的 LLM 分析层是离线模拟分析器：

- 不调用 OpenAI 或其他真实 LLM API。
- 不需要 API key。
- 不访问网络。
- 按 `skills/roi-anomaly-analysis/SKILL.md` 中沉淀的人工分析流程生成建议。
- 只分析已经被 ROI 阈值筛出的 `AlertCase`。
- 不负责判断 ROI 是否异常。

## MVP 完成情况

当前第一版 MVP 已完成：

- 已提供模拟 CSV 输入。
- 已实现确定性 ROI 阈值初筛。
- 已把异常广告整理为 `AlertCase`。
- 已沉淀项目内分析流程。
- 已实现离线 LLM 分析层。
- 已生成 Markdown 预警报告。
- 已提供基础测试。

## 后续步骤

下一步可以根据需要接入真实 LLM API，或继续完善 Markdown 报告格式。
