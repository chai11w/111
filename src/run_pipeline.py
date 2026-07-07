import argparse
from dataclasses import dataclass
from pathlib import Path

try:
    from llm_analyzer import analyze_alert_case, build_markdown_report
    from roi_filter import load_and_classify_ads
except ModuleNotFoundError:
    from src.llm_analyzer import analyze_alert_case, build_markdown_report
    from src.roi_filter import load_and_classify_ads


@dataclass(frozen=True)
class PipelineResult:
    input_path: Path
    output_path: Path
    total_alerts: int
    low_alerts: int
    high_alerts: int


def run_pipeline(input_path: Path, output_path: Path) -> PipelineResult:
    classified_ads = load_and_classify_ads(input_path)
    alert_cases = [classified_ad.to_alert_case() for classified_ad in classified_ads]
    analyses = [analyze_alert_case(alert_case) for alert_case in alert_cases]
    report = build_markdown_report(analyses, str(input_path))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    low_alerts = sum(1 for alert_case in alert_cases if alert_case.alert_type == "低效广告")
    high_alerts = sum(1 for alert_case in alert_cases if alert_case.alert_type == "优质广告")

    return PipelineResult(
        input_path=input_path,
        output_path=output_path,
        total_alerts=len(alert_cases),
        low_alerts=low_alerts,
        high_alerts=high_alerts,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="运行 ROI 异常预警 MVP 完整流程")
    parser.add_argument("--input", default="data/ad_data_sample.csv", help="输入 CSV 文件路径")
    parser.add_argument("--output", default="reports/roi_alert_report.md", help="输出 Markdown 报告路径")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_pipeline(Path(args.input), Path(args.output))
    print("ROI 异常预警 MVP 流程执行完成。")
    print(f"输入文件：{result.input_path}")
    print(f"输出报告：{result.output_path}")
    print(f"异常广告总数：{result.total_alerts}")
    print(f"低效广告：{result.low_alerts}")
    print(f"优质广告：{result.high_alerts}")


if __name__ == "__main__":
    main()
