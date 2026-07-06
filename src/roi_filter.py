import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


LOW_ROI_THRESHOLD = 1.2
HIGH_ROI_THRESHOLD = 3.0
KEY_METRIC_FIELDS = ("spend", "revenue", "orders", "clicks", "impressions", "ctr", "cpa", "roi")


@dataclass(frozen=True)
class AlertCase:
    date: str
    platform: str
    owner: str
    category: str
    campaign_name: str
    ad_name: str
    alert_type: str
    trigger_rule: str
    metrics: dict[str, float]


@dataclass(frozen=True)
class ClassifiedAd:
    row: dict
    alert_type: str
    trigger_rule: str
    row_number: int

    def to_alert_case(self) -> AlertCase:
        metrics = {
            field_name: parse_float(self.row[field_name], field_name, self.row_number)
            for field_name in KEY_METRIC_FIELDS
        }
        return AlertCase(
            date=self.row["date"],
            platform=self.row["platform"],
            owner=self.row["owner"],
            category=self.row["category"],
            campaign_name=self.row["campaign_name"],
            ad_name=self.row["ad_name"],
            alert_type=self.alert_type,
            trigger_rule=self.trigger_rule,
            metrics=metrics,
        )


def parse_float(value: str, field_name: str, row_number: int) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"第 {row_number} 行字段 {field_name} 不是有效数字：{value}") from exc


def classify_roi(roi: float, low_threshold: float, high_threshold: float) -> tuple[str, str] | None:
    if roi < low_threshold:
        return "低效广告", f"roi < {low_threshold}"
    if roi > high_threshold:
        return "优质广告", f"roi > {high_threshold}"
    return None


def load_and_classify_ads(
    csv_path: Path,
    low_threshold: float = LOW_ROI_THRESHOLD,
    high_threshold: float = HIGH_ROI_THRESHOLD,
) -> list[ClassifiedAd]:
    if low_threshold >= high_threshold:
        raise ValueError("低效 ROI 阈值必须小于优质 ROI 阈值")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if "roi" not in (reader.fieldnames or []):
            raise ValueError("CSV 缺少 roi 字段")

        classified_ads: list[ClassifiedAd] = []
        for row_number, row in enumerate(reader, start=2):
            roi = parse_float(row["roi"], "roi", row_number)
            classification = classify_roi(roi, low_threshold, high_threshold)
            if classification is None:
                continue
            alert_type, trigger_rule = classification
            classified_ads.append(
                ClassifiedAd(row=row, alert_type=alert_type, trigger_rule=trigger_rule, row_number=row_number)
            )

    return classified_ads


def print_classified_ads(classified_ads: list[ClassifiedAd]) -> None:
    if not classified_ads:
        print("未发现 ROI 异常广告。")
        return

    for ad in classified_ads:
        alert_case = ad.to_alert_case()
        print(
            f"{alert_case.alert_type} | {alert_case.platform} | {alert_case.owner} | {alert_case.category} | "
            f"{alert_case.campaign_name} | {alert_case.ad_name} | roi={alert_case.metrics['roi']} | "
            f"触发规则：{alert_case.trigger_rule}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ROI 异常广告初筛工具")
    parser.add_argument("--input", default="data/ad_data_sample.csv", help="输入 CSV 文件路径")
    parser.add_argument("--low-threshold", type=float, default=LOW_ROI_THRESHOLD, help="低效广告 ROI 阈值")
    parser.add_argument("--high-threshold", type=float, default=HIGH_ROI_THRESHOLD, help="优质广告 ROI 阈值")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    classified_ads = load_and_classify_ads(
        Path(args.input),
        low_threshold=args.low_threshold,
        high_threshold=args.high_threshold,
    )
    print_classified_ads(classified_ads)


if __name__ == "__main__":
    main()
