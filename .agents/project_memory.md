# 项目记忆

## 当前状态

- 项目路径：`F:\cc\17复试题目\执行`
- 项目目标：实现跨境电商广告数据 AI 监控与预警工具第一版 MVP。
- 当前 MVP 范围：ROI 异常预警分析模块。
- 输入：模拟 CSV 广告数据 `data/ad_data_sample.csv`。
- 输出目标：Markdown 预警报告，后续生成到 `reports/`。
- 项目内 ROI 异常分析流程：`skills/roi-anomaly-analysis/SKILL.md`。
- 当前数据字段：`date,platform,owner,category,campaign_name,ad_name,spend,revenue,orders,clicks,impressions,ctr,cpa,roi`。
- 当前模拟投手和品类：`Alice -> Beauty`、`Ben -> Electronics`、`Cindy -> Home`。
- 完整 AI 使用过程记录文件是 `.agents/codex过程记录.md`。

## 已完成

- 已建立项目上下文文件：`AGENTS.md`、`.agents/project_memory.md`、`.agents/codex过程记录.md`。
- 已创建基础项目结构：`data/`、`src/`、`reports/`、`tests/`。
- 已创建模拟广告数据：`data/ad_data_sample.csv`。
- 已实现 ROI 阈值初筛：`src/roi_filter.py`。
- 已实现异常广告结构化整理：`AlertCase` 包含 `alert_type`、`trigger_rule` 和 `metrics`。
- 已沉淀项目内分析流程：`skills/roi-anomaly-analysis/SKILL.md`。
- 已实现离线 LLM 分析层：`src/llm_analyzer.py`。
- 已实现完整 MVP 流程入口：`src/run_pipeline.py`。
- 已生成 Markdown 预警报告：`reports/roi_alert_report.md`。
- 已创建基础测试：`tests/test_roi_filter.py`。
- 已创建项目说明：`README.md`。
- 已补充 README 运行说明，明确输入、输出、运行命令和当前 LLM 为离线模拟分析器。

## 未完成

- 尚未接入真实 LLM API。
- 尚未接入真实广告平台数据。

## MVP 完成判断

- 第一版 MVP 已完成：模拟 CSV 输入、ROI 阈值初筛、异常广告结构化、离线 LLM 分析层、完整流程入口、Markdown 预警报告和基础测试都已具备。
- 当前未完成项属于 MVP 后续增强，不影响第一版 MVP 闭环。

## 关键规则

- 日常新会话只默认读取 `AGENTS.md` 和 `.agents/project_memory.md`。
- 只有用户明确要求整理提交材料、回顾历史、检查完整对话记录时，才读取 `.agents/codex过程记录.md`。
- `.agents/codex过程记录.md` 只作为作业提交材料保存；后续可以追加，但不要为了追加而全文读取。
- 新增过程记录必须使用追加写入方式，优先使用 `python scripts/append_codex_record.py`，不要用 `apply_patch` 修改 `.agents/codex过程记录.md`。
- 检查过程记录是否已追加时，只查看标题日期或文件末尾，不全文读取。
- ROI 是否异常必须由确定性阈值逻辑判断，LLM 不负责判断 ROI 是否达标。
- 当前默认阈值：`roi < 1.2` 为低效广告，`roi > 3.0` 为优质广告。
- LLM 只分析已经被阈值筛出的异常广告，并按 `skills/roi-anomaly-analysis/SKILL.md` 的流程生成原因和建议。
- 第一版 MVP 不执行预算调整，只输出预警和建议。
- 文件名、路径、命令、仓库地址保持原样，不翻译。
- 每次代码、脚本、文档、配置或项目上下文更新后，都应提交并推送到 `https://github.com/chai11w/111`。
- 上传前排除密钥、本地配置、临时文件、大型正式数据和不应公开的材料。

## 重要命令

运行 ROI 初筛：

```powershell
python src/roi_filter.py --input data/ad_data_sample.csv
```

运行测试：

```powershell
python -m unittest discover -s tests
```

生成 Markdown 预警报告：

```powershell
python src/llm_analyzer.py --input data/ad_data_sample.csv --output reports/roi_alert_report.md
```

运行完整 MVP 流程：

```powershell
python src/run_pipeline.py --input data/ad_data_sample.csv --output reports/roi_alert_report.md
```

检查版本库状态：

```powershell
git status --short --branch
```

追加过程记录：

```powershell
python scripts/append_codex_record.py --time "2026-07-06 22:00:00" --user-input "用户输入摘要" --model-output "模型输出摘要" --changed-file "文件A" --changed-file "文件B"
```

## 下一步

下一步可以根据需要接入真实 LLM API，或继续完善 Markdown 报告格式。
