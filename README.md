# ROI 异常预警分析 MVP

本项目是跨境电商广告数据 AI 监控与预警工具的第一版 MVP。

当前只实现一个最小模块：ROI 异常预警分析模块。

## MVP 边界

- 输入：模拟 CSV 广告数据，位置为 `data/ad_data_sample.csv`。
- 初筛：由确定性 ROI 阈值判断异常广告。
- LLM：不判断 ROI 是否达标，只分析已经被阈值筛出的异常广告。
- 输出：Markdown 预警报告，后续生成到 `reports/`。
- 第一版不自动调整预算，只输出预警和建议。

## 当前目录

```text
data/
  ad_data_sample.csv
src/
reports/
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

## 下一步

当前已实现 ROI 阈值初筛逻辑：

- ROI 低于低效阈值，标记为低效广告。
- ROI 高于优质阈值，标记为优质广告。
- ROI 正常，暂时不进入 LLM 分析。

默认阈值：

```text
低效广告：roi < 1.2
优质广告：roi > 3.0
```

运行初筛：

```powershell
python src/roi_filter.py --input data/ad_data_sample.csv
```

运行测试：

```powershell
python -m unittest discover -s tests
```

## 后续步骤

下一步实现 LLM 分析层。第一版可以先使用本地离线占位分析器，避免被 API key 或网络环境卡住。
