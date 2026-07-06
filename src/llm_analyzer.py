import argparse
from dataclasses import dataclass
from pathlib import Path

try:
    from roi_filter import AlertCase, load_and_classify_ads
except ModuleNotFoundError:
    from src.roi_filter import AlertCase, load_and_classify_ads


@dataclass(frozen=True)
class AlertAnalysis:
    alert_case: AlertCase
    priority: str
    possible_reasons: list[str]
    recommended_actions: list[str]
    human_check_items: list[str]


def format_number(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def decide_priority(alert_case: AlertCase) -> str:
    metrics = alert_case.metrics
    spend = metrics["spend"]
    orders = metrics["orders"]
    roi = metrics["roi"]

    if alert_case.alert_type == "低效广告":
        if spend >= 150 or roi <= 0.8:
            return "高"
        if spend >= 80 or orders >= 3:
            return "中"
        return "低"

    if spend >= 100 and orders >= 10:
        return "高"
    if spend >= 80 or orders >= 5:
        return "中"
    return "低"


def analyze_low_efficiency(alert_case: AlertCase) -> tuple[list[str], list[str], list[str]]:
    metrics = alert_case.metrics
    reasons: list[str] = []
    actions: list[str] = []
    checks: list[str] = []

    if metrics["ctr"] < 0.015:
        reasons.append("点击率偏低，可能说明素材吸引力、受众匹配或平台流量质量不足。")
        actions.append("优先复查素材首屏卖点和目标受众，准备替换素材或重新测试卖点。")

    if metrics["clicks"] >= 250 and metrics["orders"] <= 4:
        reasons.append("点击量不低但订单数偏少，可能是落地页、价格、优惠力度或购买链路影响转化。")
        actions.append("检查落地页、价格、库存、优惠和支付链路，确认点击后的转化阻塞点。")

    if metrics["cpa"] >= 35:
        reasons.append("转化成本偏高，当前花费换来的订单效率不足。")
        actions.append("让投手人工确认是否降低预算、收窄受众或暂停该广告。")

    if metrics["orders"] <= 2:
        reasons.append("订单量较少，当前数据可能存在样本量不足的问题。")
        checks.append("结合更长时间窗口复核订单量，避免只用小样本做结论。")

    if not reasons:
        reasons.append("ROI 已触发低效规则，但当前辅助指标不足以确认单一原因。")

    actions.append("保留该广告的 ROI 异常记录，进入下一轮人工复核。")
    checks.extend(["素材版本与投放人群", "落地页和商品价格", "是否存在库存、支付或优惠异常"])
    return reasons[:3], actions[:4], checks[:3]


def analyze_high_efficiency(alert_case: AlertCase) -> tuple[list[str], list[str], list[str]]:
    metrics = alert_case.metrics
    reasons: list[str] = []
    actions: list[str] = []
    checks: list[str] = []

    if metrics["orders"] >= 10 and metrics["spend"] >= 100:
        reasons.append("订单量和花费都有一定规模，当前高 ROI 相对更可信。")
        actions.append("建议人工确认后小幅提高预算，并继续观察 ROI 是否保持。")
    else:
        reasons.append("ROI 表现较好，但样本规模仍需人工复核。")
        actions.append("先小幅测试预算或延长观察窗口，不建议直接大幅放量。")

    if metrics["ctr"] >= 0.03 and metrics["cpa"] <= 12:
        reasons.append("点击率较高且转化成本较低，素材吸引和转化效率都较好。")
        actions.append("复用该广告的素材卖点、人群方向或关键词方向到新测试组。")
    elif metrics["cpa"] <= 12:
        reasons.append("转化成本较低，点击后的购买质量可能较好。")
        actions.append("保留当前投放设置，避免一次性大改导致效果波动。")

    checks.extend(["该广告是否处于稳定投放阶段", "素材卖点和人群特征", "加预算后 ROI 是否保持"])
    return reasons[:3], actions[:4], checks[:3]


def analyze_alert_case(alert_case: AlertCase) -> AlertAnalysis:
    if alert_case.alert_type == "低效广告":
        reasons, actions, checks = analyze_low_efficiency(alert_case)
    else:
        reasons, actions, checks = analyze_high_efficiency(alert_case)

    return AlertAnalysis(
        alert_case=alert_case,
        priority=decide_priority(alert_case),
        possible_reasons=reasons,
        recommended_actions=actions,
        human_check_items=checks,
    )


def format_metrics(alert_case: AlertCase) -> str:
    metrics = alert_case.metrics
    return (
        f"roi={format_number(metrics['roi'])}，"
        f"spend={format_number(metrics['spend'])}，"
        f"revenue={format_number(metrics['revenue'])}，"
        f"orders={format_number(metrics['orders'])}，"
        f"ctr={format_number(metrics['ctr'])}，"
        f"cpa={format_number(metrics['cpa'])}"
    )


def format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def build_markdown_report(analyses: list[AlertAnalysis], source_file: str) -> str:
    low_count = sum(1 for analysis in analyses if analysis.alert_case.alert_type == "低效广告")
    high_count = sum(1 for analysis in analyses if analysis.alert_case.alert_type == "优质广告")

    sections = [
        "# ROI 异常广告预警报告",
        "",
        "## 报告说明",
        "",
        f"- 数据来源：`{source_file}`",
        "- 初筛方式：确定性 ROI 阈值",
        "- 分析方式：按 `skills/roi-anomaly-analysis/SKILL.md` 的流程生成离线分析建议",
        "- 重要边界：LLM 分析层不判断 ROI 是否达标，只分析已筛出的异常广告",
        "",
        "## 汇总",
        "",
        f"- 异常广告总数：{len(analyses)}",
        f"- 低效广告：{low_count}",
        f"- 优质广告：{high_count}",
        "",
    ]

    if not analyses:
        sections.extend(["未发现 ROI 异常广告。", ""])
        return "\n".join(sections)

    sections.append("## 异常明细")
    sections.append("")
    for index, analysis in enumerate(analyses, start=1):
        alert_case = analysis.alert_case
        ad_label = (
            f"{alert_case.platform} / {alert_case.owner} / {alert_case.category} / "
            f"{alert_case.campaign_name} / {alert_case.ad_name}"
        )
        sections.extend(
            [
                f"### {index}. {ad_label}",
                "",
                f"- 异常类型：{alert_case.alert_type}",
                f"- 触发规则：{alert_case.trigger_rule}",
                f"- 关键数据：{format_metrics(alert_case)}",
                f"- 优先级：{analysis.priority}",
                "",
                "可能原因：",
                "",
                format_bullets(analysis.possible_reasons),
                "",
                "建议动作：",
                "",
                format_bullets(analysis.recommended_actions),
                "",
                "需人工确认：",
                "",
                format_bullets(analysis.human_check_items),
                "",
            ]
        )

    return "\n".join(sections).rstrip() + "\n"


def generate_report(input_path: Path, output_path: Path) -> str:
    alert_cases = [classified_ad.to_alert_case() for classified_ad in load_and_classify_ads(input_path)]
    analyses = [analyze_alert_case(alert_case) for alert_case in alert_cases]
    report = build_markdown_report(analyses, str(input_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成 ROI 异常广告 Markdown 预警报告")
    parser.add_argument("--input", default="data/ad_data_sample.csv", help="输入 CSV 文件路径")
    parser.add_argument("--output", default="reports/roi_alert_report.md", help="输出 Markdown 报告路径")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    generate_report(Path(args.input), Path(args.output))
    print(f"已生成预警报告：{args.output}")


if __name__ == "__main__":
    main()
